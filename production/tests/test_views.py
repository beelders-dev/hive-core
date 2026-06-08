from django.test import TestCase
from django.urls import reverse
from decimal import Decimal

from ..models import Recipe, RecipeIngredient
from inventory.models import Ingredient
from ..services import RecipeService


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

    def test_recipe_create_view_redirects(self):

        response = self.client.post(
            reverse("production:recipe_create"),
            data={
                "recipe_name": "Chocolate bar",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": 1,
            },
        )

        self.assertEqual(response.status_code, 302)

    def test_recipe_create_view_rejects_blank_name(self):

        with self.assertRaises(ValueError):
            self.client.post(
                reverse("production:recipe_create"),
                data={
                    "recipe_name": "",
                    "ingredient_ids": [str(self.ingredient.pk)],
                    f"quantity_{self.ingredient.pk}": 1,
                },
            )

        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipe_create_view_rejects_zero_quantity(self):

        with self.assertRaises(ValueError):
            self.client.post(
                reverse("production:recipe_create"),
                data={
                    "recipe_name": "Doughnut",
                    "ingredient_ids": [str(self.ingredient.pk)],
                    f"quantity_{self.ingredient.pk}": 0,
                },
            )

        self.assertEqual(Recipe.objects.count(), 0)
