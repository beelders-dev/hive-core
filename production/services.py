from production.models import RecipeIngredient
from inventory.models import Ingredient


class RecipeBuilder:

    SESSION_KEY = "selected_ingredients"

    def __init__(self, session):
        self.session = session

    def get_selected(self):

        return self.session.get(self.SESSION_KEY, {})

    def add(self, ingredient_id):

        selected = self.get_selected()

        ingredient_id = str(ingredient_id)
        if ingredient_id not in selected:
            selected[ingredient_id] = {"quantity": None}

        self.session[self.SESSION_KEY] = selected
        self.session.modified = True

    def get_ingredients(self):

        selected = self.get_selected()

        ingredients = Ingredient.objects.filter(id__in=selected.keys())

        for ingredient in ingredients:

            ingredient.quantity = selected.get(str(ingredient.id), {}).get(
                "quantity", ""
            )

        return ingredients

    def clear(self):
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def create_recipe_ingredients(
        self,
        recipe,
    ):
        selected = self.get_selected()

        for ingredient_id, data in selected.items():

            quantity = data.get("quantity")

            if quantity in [None, ""]:
                raise ValueError(f"Ingredient {ingredient_id} missing quantity.")

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_id,
                quantity_needed=quantity,
            )

    def remove(self, ingredient_id):
        selected = self.get_selected()

        ingredient_id = str(ingredient_id)

        del selected[ingredient_id]

        self.session[self.SESSION_KEY] = selected
        self.session.modified = True

    def update_quantity(self, ingredient_id, new_quantity):
        selected = self.get_selected()

        ingredient_id = str(ingredient_id)

        if ingredient_id in selected:
            selected[ingredient_id]["quantity"] = new_quantity

        self.session[self.SESSION_KEY] = selected
        self.session.modified = True
