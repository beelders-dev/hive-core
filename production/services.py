from decimal import Decimal
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from inventory.models import Ingredient
from .models import Recipe, RecipeIngredient


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
                quantity_needed=quantity,
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
                quantity_needed=quantity,
            )

            recipe_ingredient.full_clean()
            recipe_ingredient.save()

        return recipe


class ProductionService:

    @transaction.atomic
    def produce_recipe(self, recipe, batches=1):

        for requirement in recipe.get_all_ingredients():
            qty_to_deduct = requirement.quantity_needed * batches

            ingredient = requirement.ingredient

            if not ingredient:
                raise ValidationError("Ingredient not found.")

            if ingredient.current_stock < qty_to_deduct:
                raise ValidationError("Stock is short.")

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
