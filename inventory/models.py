import uuid
from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

# Create your models here.


class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
    )
    stock_qty = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(
                Decimal(0.01), message=("Stock quantity cannot be less than 0.01.")
            ),
        ],
    )
    UNIT_CHOICES = {"g": "Grams", "ml": "Mililiter"}
    unit = models.CharField(max_length=2, choices=UNIT_CHOICES, default="g")
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        validators=[
            MinValueValidator(
                Decimal(0.01), message=("Price cannot be less than 0.01.")
            ),
        ],
    )

    def get_total_amount(self):
        return self.stock_qty * self.price

    def __str__(self):
        return f"{self.name}  ({self.stock_qty:.2f}g)"

    def get_absolute_url(self):
        return reverse("inventory:ingredient", kwargs={"pk": self.pk})
