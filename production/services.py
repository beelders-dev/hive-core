from .models import Recipe, RecipeIngredient
from django.db import transaction
from decimal import Decimal


class RecipeService:

    @transaction.atomic()
    def create_recipe(self, recipe_name, ingredients):

        recipe_name = recipe_name.strip()

        if not recipe_name:
            raise ValueError("Recipe name is required.")

        recipe = Recipe.objects.create(name=recipe_name)

        if not ingredients:
            raise ValueError("You need at least 1 ingredient.")

        for ingredient in ingredients:

            ingredient_id = ingredient["ingredient_id"]
            quantity = Decimal(ingredient["quantity"], None)

            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_id,
                quantity_needed=quantity,
            )
