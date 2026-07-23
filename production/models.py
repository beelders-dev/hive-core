import uuid
from datetime import timedelta
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipe",
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        error_messages={
            "blank": "Recipe name cannot be blank.",
            "max_length": "Max characters for recipe name: 100",
        },
    )
    description = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField(
        "inventory.Ingredient",
        through="RecipeIngredient",
    )

    def get_absolute_url(self):
        return reverse("production:recipe", kwargs={"pk": self.pk})

    def get_all_ingredients(self):
        return self.ingredient_requirements.all()

    def __str__(self):
        return f"{self.name}"

    def get_ingredient_ids(self):
        return self.get_all_ingredients().values_list("ingredient_id", flat=True)

    @property
    def total_cost(self):
        total_cost = 0
        for ingredient in self.get_all_ingredients():
            total_cost += ingredient.ingredient_cost
        return total_cost

    @property
    def is_recently_added(self):
        return self.created_at >= timezone.now() - timedelta(days=15)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        "recipe",
        on_delete=models.CASCADE,
        related_name="ingredient_requirements",
    )

    ingredient = models.ForeignKey(
        "inventory.Ingredient",
        on_delete=models.CASCADE,
    )
    qty_needed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal("0.01"),
                message="Quantity must be greater than or equal to 0.01.",
            )
        ],
    )

    @property
    def ingredient_cost(self):
        return self.ingredient.average_unit_cost * self.qty_needed


class ProductionBatch(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="production_batches",
    )
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.SET_NULL,
        related_name="batches",
        null=True,
        blank=True,
    )

    batch_qty = models.IntegerField()
    notes = models.TextField(blank=True, null=True)

    recipe_name = models.CharField(max_length=100)
    est_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    class Status(models.TextChoices):
        PENDING = "P", "Pending"
        IN_PROGRESS = "I", "In Progress"
        COMPLETE = "C", "Complete"
        CANCELLED = "X", "Cancelled"

    status = models.CharField(
        max_length=1,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    cancelled_at = models.DateTimeField(null=True)
    completed_at = models.DateTimeField(null=True)

    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="products",
        null=True,
        blank=True,
    )

    cancellation_note = models.TextField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("batch_detail", kwargs={"pk": self.pk})


class BatchIngredient(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    production_batch = models.ForeignKey(
        ProductionBatch, on_delete=models.CASCADE, related_name="batch_ingredients"
    )

    ingredient = models.ForeignKey(
        "inventory.Ingredient", on_delete=models.CASCADE, blank=True, null=True
    )

    ingredient_name_snapshot = models.CharField(max_length=100)
    unit_snapshot = models.CharField(max_length=20)

    qty_used = models.DecimalField(max_digits=10, decimal_places=2)
    unit_cost_snapshot = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
