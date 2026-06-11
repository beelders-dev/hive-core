from django.test import TestCase
from django.urls import reverse


from ..models import Recipe
from inventory.models import Ingredient


class ViewTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Cocoa Powder")

    def test_recipe_list_view_loads_correctly(self):
        response = self.client.get(reverse("production:recipe_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/recipe_list.html")

    def test_recipe_detail_view_loads_correctly(self):
        recipe = Recipe.objects.create(name="Chocolate bar")
        response = self.client.get(reverse("production:recipe", args=[recipe.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["recipe"], recipe)
        self.assertTemplateUsed(response, "production/recipe/recipe_detail.html")

    def test_recipe_create_view_loads_correctly(self):
        response = self.client.get(reverse("production:recipe_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/recipe_form.html")

    def test_recipe_create_view_creates_ingredient_successfully(self):

        response = self.client.post(
            reverse("production:recipe_create"),
            data={
                "recipe_name": "Chocolate bar",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": 1,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Recipe.objects.count(), 1)
