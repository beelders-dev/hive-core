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

    UNIT_CHOICES = {"g": "Grams", "ml": "Mililiters"}
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default="g")

    low_stock_threshold = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
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


class IngredientPurchase(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name="purchases"
    )
    purchased_at = models.DateField()
    exp_date = models.DateField(blank=True, null=True)
    qty_purchased = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01"), message=("Must be at least 0.01.")),
        ],
    )
    qty_remaining = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    total_cost = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.01"), message=("Must be at least 0.01."))
        ],
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.qty_remaining = self.qty_purchased

        super().save(*args, **kwargs)

    @property
    def unit_cost(self):
        if self.qty_purchased == 0:
            return Decimal("0")

        return self.total_cost / self.qty_purchased
