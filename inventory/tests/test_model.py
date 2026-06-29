from django.core.exceptions import ValidationError
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Ingredient


class IngredientModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="mike", password="testpass123"
        )
        self.ingredient = Ingredient.objects.create(
            user=self.user, name="Egg", unit="g", low_stock_threshold="0"
        )

    def test_ingredient_content(self):
        self.assertEqual(self.ingredient.name, "Egg")

    def test_get_absolute_url_returns_correct_url(self):
        self.assertEqual(
            self.ingredient.get_absolute_url(),
            reverse("inventory:ingredient", kwargs={"pk": self.ingredient.pk}),
        )
