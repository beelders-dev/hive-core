from production.models import RecipeIngredient, Recipe
from inventory.models import Ingredient
from decimal import Decimal, InvalidOperation
from django.db import transaction


class RecipeBuilder:

    SESSION_KEY = "recipe_draft"

    def __init__(self, session):
        self.session = session

    def get_draft(self):
        draft = self.session.get(self.SESSION_KEY, {})

        draft.setdefault("name", "")
        draft.setdefault("ingredients", {})

        return draft

    def add(self, ingredient_id):
        draft = self.get_draft()

        ingredient_id = str(ingredient_id)

        if ingredient_id not in draft["ingredients"]:
            draft["ingredients"][ingredient_id] = {"required_quantity": None}

        self.session[self.SESSION_KEY] = draft
        self.session.modified = True

    def get_ingredients(self):
        draft = self.get_draft()

        ingredients = Ingredient.objects.filter(id__in=draft["ingredients"].keys())

        for ingredient in ingredients:

            ingredient.required_quantity = (
                draft["ingredients"]
                .get(str(ingredient.id), {})
                .get("required_quantity", "")
            )

        return ingredients

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def remove(self, ingredient_id):
        draft = self.get_draft()

        ingredient_id = str(ingredient_id)

        del draft["ingredients"][ingredient_id]

        self.session[self.SESSION_KEY] = draft
        self.session.modified = True

    def update_quantity(self, ingredient_id, new_quantity):
        draft = self.get_draft()

        ingredient_id = str(ingredient_id)

        if ingredient_id in draft["ingredients"]:
            draft["ingredients"][ingredient_id]["required_quantity"] = new_quantity

        self.session[self.SESSION_KEY] = draft
        self.session.modified = True

    def update_name(self, new_name):
        draft = self.get_draft()
        draft["name"] = new_name

        self.session[self.SESSION_KEY] = draft
        self.session.modified = True

    def get_name(self):
        draft = self.get_draft()

        return draft.get("name", "")


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
