import uuid
from django.db import models
from django.urls import reverse

# Create your models here.


class Ingredient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    stock_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name}  ({self.stock_qty}g)"

    def get_absolute_url(self):
        return reverse("inventory:ingredient", kwargs={"pk": self.pk})
