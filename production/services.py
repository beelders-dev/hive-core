from production.models import RecipeIngredient
from inventory.models import Ingredient


class RecipeBuilder:

    SESSION_KEY = "selected_ingredients"

    def __init__(self, session):
        self.session = session

    def get_selected(self):
        return self.session.get(self.SESSION_KEY, [])

    def add(self, ingredient_id):
        selected = self.get_selected()

        ingredient_id = str(ingredient_id)

        if ingredient_id not in selected:
            selected.append(ingredient_id)

        self.session[self.SESSION_KEY] = selected

    def get_ingredients(self):
        selected = self.get_selected()

        return Ingredient.objects.filter(id__in=selected)

    def clear(self):
        self.session[self.SESSION_KEY] = []

    def create_recipe_ingredients(
        self,
        recipe,
        post_data,
    ):
        selected = self.get_selected()

        for ingredient_id in selected:
            quantity = post_data.get(f"quantity_{ingredient_id}")
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

        selected.remove(ingredient_id)

        self.session[self.SESSION_KEY] = selected
        self.session.modified = True
