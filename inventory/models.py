import uuid
from decimal import Decimal

from django.db.models import Sum
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.


class Ingredient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ingredients",
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    modified_at = models.DateTimeField(auto_now=True)

    UNIT_CHOICES = {"g": "Grams", "ml": "Mililiters"}
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default="g")

    low_stock_threshold = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        validators=[
            MinValueValidator(
                Decimal("0"), message="Stock threshold cannot be negative."
            )
        ],
    )

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse("inventory:ingredient", kwargs={"pk": self.pk})

    @property
    def current_stock(self):
        return self.purchases.aggregate(total=Sum("qty_remaining"))["total"] or Decimal(
            "0"
        )

    @property
    def total_inventory_value(self):
        total = Decimal("0")

        for purchase in self.purchases.all():
            total += purchase.unit_cost * purchase.qty_remaining

        return total

    @property
    def average_unit_cost(self):
        if self.current_stock == 0:
            return Decimal("0")
        return self.total_inventory_value / self.current_stock

    @property
    def is_out_of_stock(self):
        return self.current_stock == 0

    @property
    def is_low_stock(self):
        return self.current_stock > 0 and self.current_stock <= self.low_stock_threshold

    @property
    def stock_status(self):
        if self.is_out_of_stock:
            return "out"
        elif self.is_low_stock:
            return "low"
        else:
            return "in"

    @property
    def short_id(self):
        return str(self.id)[:8].upper()


class IngredientPurchase(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="purchases"
    )
    modified_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    purchased_at = models.DateField()
    exp_date = models.DateField(blank=True, null=True)
    qty_purchased = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("0.01"), message=("Purchased quantity must be at least 0.01.")
            ),
        ],
    )
    qty_remaining = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    total_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("0.01"), message=("Total cost must be at least 0.01.")
            )
        ],
    )

    def __str__(self):
        return self.short_id

    @property
    def short_id(self):
        return str(self.id)[:8].upper()

    @property
    def unit_cost(self):
        if self.qty_purchased == 0:
            return Decimal("0")

        return self.total_cost / self.qty_purchased

    @property
    def get_stock_difference(self):
        return self.qty_purchased - self.qty_remaining

    @property
    def total_stock_adjustments(self):
        return self.adjustments.aggregate(total=Sum("qty_adjustment"))[
            "total"
        ] or Decimal("0")

    @property
    def total_adjustment_value(self):
        return self.total_stock_adjustments * self.unit_cost

    @property
    def current_inventory_value(self):
        return self.total_cost + self.total_adjustment_value

    @property
    def total_stocks_plus_adjustments(self):
        return self.qty_remaining + self.total_stock_adjustments

    def save(self, *args, **kwargs):
        """
        Initialize qty_remaining to the purchased quantity when creating a new
        purchase record.

        This ensures that newly created purchases start with all purchased stock
        available. On subsequent saves, qty_remaining is left unchanged to
        preserve any deductions made through inventory consumption.
        """

        if self._state.adding:
            self.qty_remaining = self.qty_purchased

        super().save(*args, **kwargs)


class PurchaseAdjustment(models.Model):
    purchase = models.ForeignKey(
        IngredientPurchase, on_delete=models.CASCADE, related_name="adjustments"
    )
    qty_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.CharField(
        max_length=500,
    )

    @property
    def adjustment_value(self):
        return self.qty_adjustment * self.purchase.unit_cost
