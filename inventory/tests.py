from django.test import TestCase
from django.urls import reverse

from .models import Ingredient

# Create your tests here.


class IngredientTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ingredient = Ingredient.objects.create(
            name="egg", stock_qty=12.00, price=25.00
        )

    # Model tests
    def test_ingredient_content(self):
        """Test that model fields save correctly"""
        self.assertEqual(self.ingredient.name, "egg")
        self.assertEqual(self.ingredient.stock_qty, 12.00)
        self.assertEqual(self.ingredient.price, 25.00)

    # View tests
    def test_ingredient_list_view(self):
        response = self.client.get(reverse("inventory:ingredient_list"))
        self.assertEqual(response.status_code, 200)
