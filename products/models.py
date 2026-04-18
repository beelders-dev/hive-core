import uuid
from django.db import models
from django.urls import reverse


# Create your models here.


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    short_description = models.CharField(max_length=255, blank=True)
    full_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["name"], name="name_idx"),
        ]

    def get_absolute_url(self):
        return reverse("product_detail", args=[str(self.id)])

    def __str__(self):
        return self.name
