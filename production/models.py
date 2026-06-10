import uuid
from django.urls import reverse
from django.db import models


# Create your models here.
class Recipe(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField(
        "inventory.Ingredient", through="RecipeIngredient"
    )

    def get_absolute_url(self):
        return reverse("production:recipe", kwargs={"pk": self.pk})

    def get_all_ingredients(self):
        return self.ingredient_requirements.all()

    def __str__(self):
        return f"{self.name}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        "recipe",
        on_delete=models.CASCADE,
        related_name="ingredient_requirements",
    )

    ingredient = models.ForeignKey("inventory.Ingredient", on_delete=models.CASCADE)
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2)
