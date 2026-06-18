from django.test import TestCase
from django.urls import reverse


from ..models import Recipe
from inventory.models import Ingredient


class DetailViewTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Cocoa Powder")

    def test_recipe_detail_view_loads_correctly(self):
        recipe = Recipe.objects.create(name="Chocolate bar")
        response = self.client.get(reverse("production:recipe", args=[recipe.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["recipe"], recipe)
        self.assertTemplateUsed(response, "production/recipe/recipe_detail.html")
