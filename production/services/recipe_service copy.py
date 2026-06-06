from decimal import Decimal, InvalidOperation
from ..models import RecipeIngredient, Recipe
from django.db import transaction

from .recipe_builder import RecipeBuilder


class RecipeService:

    def __init__(self, session):
        self.builder = RecipeBuilder(session)

    @transaction.atomic
    def create_recipe(self):
        draft = self.builder.get_draft()
        self.validate_draft(draft)
        recipe = Recipe.objects.create(name=draft["name"])
        self.create_ingredients(recipe, draft)
        self.builder.clear()

    def validate_draft(self, draft):

        for ingredient_id, data in draft["ingredients"].items():
            quantity = data.get("required_quantity")

            try:
                quantity = Decimal(quantity)
            except (TypeError, InvalidOperation):
                raise ValueError(f"Ingredient {ingredient_id} missing quantity")

            if quantity <= 0:
                raise ValueError(
                    f"Ingredient {ingredient_id} quantity must be greater than 0."
                )

    def create_ingredients(self, recipe, draft):

        for ingredient_id, data in draft["ingredients"].items():

            quantity = Decimal(data["required_quantity"])

            RecipeIngredient.objects.create(
                recipe=recipe, ingredient_id=ingredient_id, quantity_needed=quantity
            )
