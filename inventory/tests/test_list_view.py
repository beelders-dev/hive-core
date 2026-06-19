from django.test import TestCase
from django.urls import reverse

from ..models import Ingredient


class IngredientListViewTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Egg", stock_qty=10, price=20)
        self.url = reverse("inventory:ingredient_list")
        self.response = self.client.get(self.url)

    def test_list_view_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "inventory/ingredient_list.html")

    def test_list_view_displays_ingredients(self):
        ingredients = self.response.context["ingredient_list"]
        self.assertEqual(len(ingredients), 1)
