from django.core.exceptions import ValidationError
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse

from .models import Ingredient

# Create your tests here.


class IngredientModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ingredient = Ingredient.objects.create(
            name="egg", stock_qty=12.00, price=25.00
        )

    def test_ingredient_content(self):
        self.assertEqual(self.ingredient.name, "egg")
        self.assertEqual(self.ingredient.stock_qty, Decimal(12.00))
        self.assertEqual(self.ingredient.price, Decimal(25.00))

    def test_ingredient_str(self):
        expected = "egg  (12.00g)"
        self.assertEqual(str(self.ingredient), expected)

    def test_get_absolute_url(self):
        self.assertEqual(
            self.ingredient.get_absolute_url(),
            reverse("inventory:ingredient", kwargs={"pk": self.ingredient.pk}),
        )

    def test_get_total_amount(self):
        self.assertEqual(self.ingredient.get_total_amount(), Decimal(300.00))

    def test_stock_cannot_be_negative(self):
        invalid_ingredient = Ingredient.objects.create(
            name="apple", stock_qty=-20.00, price=25.00
        )
        with self.assertRaises(ValidationError):
            invalid_ingredient.full_clean()

    def test_price_cannot_be_negative(self):
        invalid_ingredient = Ingredient.objects.create(
            name="apple", stock_qty=20.00, price=-25.00
        )
        with self.assertRaises(ValidationError):
            invalid_ingredient.full_clean()


class IngredientViewTests(TestCase):

    @classmethod
    def setUp(self):
        self.response = self.client.get(reverse("inventory:ingredient_list"))

    def test_ingredient_list_view_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_ingredient_list_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "inventory/ingredient_list.html")

    def test_ingredient_list_displays_ingredients(self):

        Ingredient.objects.create(name="Egg", stock_qty=10, price=20)
        response = self.client.get(reverse("inventory:ingredient_list"))
        ingredients = response.context["ingredient_list"]
        self.assertEqual(len(ingredients), 1)
