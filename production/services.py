from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError


from .models import Recipe, RecipeIngredient, ProductionBatch, BatchIngredient


class RecipeService:

    INGREDIENT_VALIDATION_ERROR = "Add at least 1 ingredient."

    @staticmethod
    @transaction.atomic()
    def create_recipe(recipe, ingredients):

        if not ingredients:
            raise ValidationError(RecipeService.INGREDIENT_VALIDATION_ERROR)

        for ingredient in ingredients:
            ingredient_id = ingredient["ingredient_id"]
            quantity = Decimal(ingredient["quantity"])

            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient_id,
                qty_needed=quantity,
            )

            recipe_ingredient.full_clean()
            recipe_ingredient.save()

    @staticmethod
    @transaction.atomic()
    def update_recipe(
        recipe,
        new_ingredients,
    ):

        recipe.get_all_ingredients().delete()

        if not new_ingredients:

            raise ValidationError(RecipeService.INGREDIENT_VALIDATION_ERROR)

        for ingredient in new_ingredients:

            ingredient_id = ingredient["ingredient_id"]
            quantity = Decimal(ingredient["quantity"])

            recipe_ingredient = RecipeIngredient(
                recipe=recipe,
                ingredient_id=ingredient_id,
                qty_needed=quantity,
            )
            recipe_ingredient.full_clean()
            recipe_ingredient.save()


class ProductionService:

    @staticmethod
    @transaction.atomic
    def produce_recipe(recipe, batch_qty=1):

        requirements = list(recipe.get_all_ingredients())

        ProductionService.deduct_ingredients(requirements)
        ProductionService.create_batch(recipe, requirements, batch_qty)

    @staticmethod
    def deduct_ingredients(requirements, batch_qty=1):

        for requirement in requirements:
            qty_to_deduct = requirement.qty_needed * batch_qty

            ingredient = requirement.ingredient

            if not ingredient:
                raise ValidationError("Ingredient not found.")

            if ingredient.current_stock < qty_to_deduct:
                raise ValidationError("Insufficient stock.")

            for purchase in ingredient.purchases.order_by("purchased_at"):

                if qty_to_deduct <= 0:
                    break

                if purchase.qty_remaining >= qty_to_deduct:
                    purchase.qty_remaining -= qty_to_deduct
                    qty_to_deduct = 0
                    purchase.save()

                else:
                    qty_to_deduct -= purchase.qty_remaining
                    purchase.qty_remaining = 0
                    purchase.save()

    @staticmethod
    def create_batch(recipe, requirements, batch_qty):
        production_batch = ProductionBatch.objects.create(
            user=recipe.user,
            recipe=recipe,
            recipe_name=recipe.name,
            batch_qty=batch_qty,
            notes=recipe.description,
            est_cost=recipe.total_cost,
        )

        requirements = recipe.get_all_ingredients()

        BatchIngredient.objects.bulk_create(
            BatchIngredient(
                production_batch=production_batch,
                ingredient=recipe_ingredient.ingredient,
                ingredient_name_snapshot=recipe_ingredient.ingredient.name,
                unit_snapshot=recipe_ingredient.ingredient.unit,
                qty_used=recipe_ingredient.qty_needed * batch_qty,
                unit_cost_snapshot=recipe_ingredient.ingredient.average_unit_cost,
                total_cost=recipe_ingredient.ingredient_cost,
            )
            for recipe_ingredient in requirements
        )

    @transaction.atomic
    def reinstate(self, batch_ingredient, batch_qty=1):

        qty_to_reinstate = batch_ingredient.qty_used * batch_qty

        # If all purchases are full, then, create a new purchase instead of raising an error.

        for purchase in batch_ingredient.ingredient.purchases.order_by("purchased_at"):

            if purchase.get_stock_difference <= qty_to_reinstate:
                purchase.qty_remaining += qty_to_reinstate
                qty_to_reinstate = 0
                purchase.save()

            else:
                purchase.qty_remaining = purchase.qty_purchased
                qty_to_reinstate = purchase.get_stock_difference
                purchase.save()
