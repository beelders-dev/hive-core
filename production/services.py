from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from inventory.models import Ingredient
from .models import Recipe, RecipeIngredient, ProductionBatch, BatchIngredient


class RecipeService:

    @transaction.atomic()
    def create_recipe(self, user, recipe_name, recipe_description, ingredients):

        recipe_name = recipe_name.strip()

        if not ingredients:
            raise ValidationError({"ingredients": ["Add at least 1 ingredient."]})

        recipe = Recipe(user=user, name=recipe_name, description=recipe_description)
        recipe.full_clean()
        recipe.save()

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
        return recipe

    def update_recipe(
        self,
        recipe,
        new_recipe_name,
        new_recipe_description,
        new_ingredients,
    ):

        new_recipe_name = new_recipe_name.strip()

        if not new_ingredients:
            raise ValidationError({"ingredients": ["Add at least 1 ingredient."]})

        recipe.name = new_recipe_name
        recipe.description = new_recipe_description

        recipe.full_clean()
        recipe.save()

        recipe.get_all_ingredients().delete()

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

        return recipe


class ProductionService:

    @transaction.atomic
    def deduct_ingredients(self, recipe, batch_qty=1):

        for requirement in recipe.get_all_ingredients():
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

    @transaction.atomic
    def produce_recipe(self, recipe, batch_qty=1):

        self.deduct_ingredients(recipe)

        production_batch = ProductionBatch.objects.create(
            user=recipe.user,
            recipe=recipe,
            recipe_name=recipe.name,
            batch_qty=batch_qty,
            notes=recipe.description,
            est_cost=recipe.total_cost,
        )

        for recipe_ingredient in recipe.get_all_ingredients():
            BatchIngredient.objects.create(
                production_batch=production_batch,
                ingredient=recipe_ingredient.ingredient,
                ingredient_name_snapshot=recipe_ingredient.ingredient.name,
                unit_snapshot=recipe_ingredient.ingredient.unit,
                qty_used=recipe_ingredient.qty_needed,
                unit_cost_snapshot=recipe_ingredient.ingredient.average_unit_cost,
                total_cost=recipe_ingredient.ingredient_cost,
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
