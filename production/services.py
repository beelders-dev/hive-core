from .models import Recipe, RecipeIngredient
from django.db import transaction
from decimal import Decimal
from django.core.exceptions import ValidationError


class RecipeService:

    @transaction.atomic()
    def create_recipe(self, recipe_name, recipe_description, ingredients):

        recipe_name = recipe_name.strip()

        if not ingredients:
            raise ValidationError({"ingredients": ["Add at least 1 ingredient."]})

        recipe = Recipe(name=recipe_name, description=recipe_description)
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
