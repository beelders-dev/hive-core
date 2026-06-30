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
        null=True,
        blank=True,
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
    quantity_needed = models.DecimalField(
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
        return self.ingredient.average_unit_cost * self.quantity_needed
