from django.test import TestCase
from django.urls import reverse

from ..models import Recipe, RecipeIngredient
from inventory.models import Ingredient


class ViewTests(TestCase):

    def setUp(self):
        pass

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

    def test_recipe_create_view_creates_recipe(self):
        ingredient = Ingredient.objects.create(name="Cocoa Powder")

        # Arrange session (required dependency)
        session = self.client.session

        session["draft"] = {
            "name": "Chocolate Bar",
            "ingredients": {str(ingredient.id): {"required_quantity": "2"}},
        }
        session.save()

        # Act
        self.client.post(reverse("production:recipe_create"))

        # Assert
        self.assertTrue(Recipe.objects.filter(name="Chocolate Bar").exists())
