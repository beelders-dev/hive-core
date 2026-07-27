from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from .models import Ingredient, IngredientPurchase, PurchaseAdjustment


class IngredientModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.flour = Ingredient.objects.create(
            user=self.user,
            name="Flour",
            unit="g",
        )

        self.cocoa_powder = Ingredient.objects.create(
            user=self.user,
            name="Cocoa Powder",
            unit="g",
        )

        IngredientPurchase.objects.create(
            ingredient=self.flour,
            purchased_at=timezone.now(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )

        IngredientPurchase.objects.create(
            ingredient=self.flour,
            purchased_at=timezone.now(),
            qty_purchased=Decimal("200"),
            total_cost=Decimal("200"),
        )

    def test_string_representation_returns_name(self):
        self.assertEqual(str(self.flour), "Flour")

    def test_get_absolute_url_returns_correct_url(self):
        self.assertEqual(
            self.flour.get_absolute_url(),
            reverse("inventory:ingredient", kwargs={"pk": self.flour.pk}),
        )

    def test_current_stock_returns_total_remaining_stock(self):
        self.assertEqual(self.flour.current_stock, Decimal("300"))

    def test_total_inventory_value_returns_correct_calculation(self):
        self.assertEqual(self.flour.total_inventory_value, Decimal("300"))

    def test_average_unit_cost_returns_correct_calculation(self):
        self.assertEqual(self.flour.average_unit_cost, Decimal("1"))

    def test_average_unit_cost_returns_zero_when_zero_stock(self):
        self.assertEqual(self.cocoa_powder.average_unit_cost, Decimal("0"))

    def test_is_out_of_stock_returns_true(self):
        self.assertTrue(self.cocoa_powder.is_out_of_stock)

    def test_is_out_of_stock_returns_false_when_stock_exists(self):
        self.assertFalse(self.flour.is_out_of_stock)

    def test_is_low_stock_returns_true_when_stock_is_below_threshold(self):
        self.flour.low_stock_threshold = Decimal("400")
        self.assertTrue(self.flour.is_low_stock)

    def test_is_low_stock_returns_true_when_stock_equals_threshold(self):
        self.flour.low_stock_threshold = Decimal("300")

        self.assertTrue(self.flour.is_low_stock)

    def test_is_low_stock_returns_false_when_stock_exceeds_threshold(self):
        self.flour.low_stock_threshold = Decimal("200")
        self.assertFalse(self.flour.is_low_stock)

    def test_stock_status_returns_LOW_when_low_stock(self):
        self.flour.low_stock_threshold = Decimal("400")
        self.assertEqual(self.flour.stock_status, "low")

    def test_stock_status_returns_IN_when_in_stock(self):
        self.assertEqual(self.flour.stock_status, "in")

    def test_stock_status_returns_OUT_when_out_of_stock(self):
        self.assertEqual(self.cocoa_powder.stock_status, "out")


class IngredientPurchaseTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.ingredient = Ingredient.objects.create(
            user=self.user,
            name="Flour",
            unit="g",
        )

        self.purchase = IngredientPurchase.objects.create(
            ingredient=self.ingredient,
            purchased_at=timezone.now(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )

    def test_string_representation_returns_short_id(self):
        self.assertEqual(str(self.purchase), self.purchase.short_id)

    def test_short_id_returns_first_eight_characters_in_uppercase(self):
        expected = str(self.purchase.id)[:8].upper()
        self.assertEqual(self.purchase.short_id, expected)

    def test_unit_cost_returns_correct_calculation(self):
        self.assertEqual(self.purchase.unit_cost, Decimal("1"))

    def test_unit_cost_returns_zero_when_qty_purchased_is_zero(self):
        self.purchase.qty_purchased = Decimal("0")
        self.assertEqual(self.purchase.unit_cost, Decimal("0"))

    def test_get_stock_difference_returns_correct_calculation(self):
        self.purchase.qty_remaining -= Decimal("50")
        self.assertEqual(self.purchase.get_stock_difference, Decimal("50"))

    def test_get_stock_difference_returns_correct_calculation_when_consumed(self):
        self.purchase.qty_remaining = Decimal("50")
        self.assertEqual(self.purchase.get_stock_difference, Decimal("50"))

    def test_total_stock_adjustments_return_correct_total_stock_adjustments(self):
        PurchaseAdjustment.objects.create(
            purchase=self.purchase, qty_adjustment=Decimal("100")
        )
        self.assertEqual(self.purchase.total_adjustment_value, Decimal("100"))

    def test_total_adjustment_value_returns_correct_calculation(self):
        PurchaseAdjustment.objects.create(
            purchase=self.purchase, qty_adjustment=Decimal("100")
        )
        self.assertEqual(self.purchase.total_stock_adjustments, Decimal("100"))

    def test_total_adjustment_value_returns_zero_when_no_adjustments_exist(self):
        self.assertEqual(
            self.purchase.total_adjustment_value,
            Decimal("0"),
        )

    def test_current_inventory_value_returns_correct_total_value(self):
        PurchaseAdjustment.objects.create(
            purchase=self.purchase, qty_adjustment=Decimal("100")
        )

        self.assertEqual(self.purchase.current_inventory_value, Decimal("200"))

    def test_total_stocks_plus_adjustments_returns_correct_total(self):
        PurchaseAdjustment.objects.create(
            purchase=self.purchase, qty_adjustment=Decimal("50")
        )
        PurchaseAdjustment.objects.create(
            purchase=self.purchase, qty_adjustment=Decimal("50")
        )
        self.assertEqual(self.purchase.total_stocks_plus_adjustments, Decimal("200"))

    def test_qty_remaining_is_initialized_to_qty_purchased(self):
        self.assertEqual(self.purchase.qty_remaining, Decimal("100"))


class PurchaseAdjustmentTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.ingredient = Ingredient.objects.create(
            user=self.user,
            name="Flour",
            unit="g",
        )

        self.purchase = IngredientPurchase.objects.create(
            ingredient=self.ingredient,
            purchased_at=timezone.now(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )

    def test_adjustment_value(self):
        adjustment = PurchaseAdjustment.objects.create(
            purchase=self.purchase, qty_adjustment=Decimal("50")
        )
        self.assertEqual(adjustment.adjustment_value, Decimal("50"))
