from django.test import TestCase
from django.urls import reverse

from ..models import Ingredient


class IngredientFieldValidators(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Egg", stock_qty=10, price=20)
        self.url = reverse("inventory:ingredient_add")

    def test_qty_field_validator_displays_error_when_qty_is_zero(self):

        response = self.client.post(
            self.url,
            data={
                "name": "Sample",
                "unit": "g",
                "stock_qty": 0,
                "price": 20,
            },
        )
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertContains(response, "Stock quantity cannot be less than 0.01.")

    def test_qty_field_validator_displays_error_when_price_is_zero(self):

        response = self.client.post(
            self.url,
            data={
                "name": "Sample",
                "unit": "g",
                "stock_qty": 1,
                "price": 0,
            },
        )
        self.assertEqual(Ingredient.objects.count(), 1)
        self.assertContains(response, "Price cannot be less than 0.01.")
