from .models import Recipe, RecipeIngredient
from django.db import transaction


class RecipeService:

    @transaction.atomic()
    def create_recipe(self, recipe_name, ingredients):

        recipe_name = recipe_name.strip()

        if not recipe_name:
            raise ValueError("Recipe name is required.")

        recipe = Recipe.objects.create(name=recipe_name)

        for ingredient in ingredients:

            ingredient_id = ingredient["ingredient_id"]
            quantity = ingredient["quantity"]

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_id,
                quantity_needed=quantity,
            )
