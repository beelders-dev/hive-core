from .models import Recipe, RecipeIngredient


class RecipeService:
    def create_recipe(self, recipe_name, ingredients):

        recipe = Recipe.objects.create(name=recipe_name)

        for ingredient in ingredients:

            ingredient_id = ingredient["ingredient_id"]
            quantity = ingredient["quantity"]

            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient_id,
                quantity_needed=quantity,
            )
