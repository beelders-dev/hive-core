from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Ingredient, IngredientPurchase


class IngredientPurchaseTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(
            username="mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(
            user=self.user, name="Cocoa powder", unit="g", low_stock_threshold="1000"
        )
        self.url = reverse(
            "inventory:ingredient_purchase_create", kwargs={"pk": self.ingredient.pk}
        )

    def test_purchase_row_is_created(self):
        self.client.post(
            self.url,
            data={
                "purchased_at": "2026-06-30",
                "qty_purchased": "2000",
                "total_cost": "200",
            },
        )

        purchase = IngredientPurchase.objects.get(ingredient=self.ingredient)

        self.assertEqual(purchase.ingredient, self.ingredient)
        self.assertEqual(purchase.purchased_at, date(2026, 6, 30))
        self.assertEqual(purchase.qty_purchased, Decimal("2000"))
        self.assertEqual(purchase.total_cost, Decimal("200"))
