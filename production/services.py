from production.models import RecipeIngredient
from inventory.models import Ingredient


class RecipeBuilder:

    SESSION_KEY = "selected_ingredients"

    def __init__(self, session):
        self.session = session

    def get_selected(self):

        selected = self.session.get(self.SESSION_KEY, {})

        if isinstance(selected, list):

            selected = {str(i): {"quantity": None} for i in selected}

            self.session[self.SESSION_KEY] = selected
            self.session.modified = True

        return selected

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

    def create_recipe_ingredients(
        self,
        recipe,
        post_data,
    ):
        selected = self.get_selected()

        for ingredient_id in selected:
            quantity = post_data.get("quantity")
            print(post_data)
            print("SESSION: ", self.get_selected())
            if not quantity:
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
