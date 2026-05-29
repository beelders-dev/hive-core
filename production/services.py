from production.models import RecipeIngredient
from inventory.models import Ingredient


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
        print("EMPTY?", draft)

        ingredients = Ingredient.objects.filter(id__in=draft["ingredients"].keys())

        for ingredient in ingredients:

            ingredient.required_quantity = (
                draft["ingredients"]
                .get(str(ingredient.id), {})
                .get("required_quantity", "")
            )

        return ingredients

    def clear(self):
        self.session.flush()
        self.session[self.SESSION_KEY] = {}
        self.session.modified = True

    def create_recipe_ingredients(
        self,
        recipe,
    ):
        draft = self.get_draft()

        for ingredient_id, data in draft["ingredients"].items():
            quantity = data.get("required_quantity")

            if quantity in [None, "", 0]:
                raise ValueError(f"Ingredient {ingredient_id} missing quantity.")

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_id,
                quantity_needed=quantity,
            )

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
