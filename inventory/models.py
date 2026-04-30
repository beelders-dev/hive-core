import uuid
from django.db import models
from django.urls import reverse

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    stock_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.name}  ({self.stock_qty}g)"


class Recipe(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField(Ingredient, through="RecipeIngredient")

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})

    # def get_recipe_breakdown(self):
    #     return {
    #         "direct": self.ingredient_requirements.all(),
    #         "sub_components": [
    #             {
    #                 "name": bridge.child_recipe.name,
    #                 "qty": bridge.quantity_needed,
    #                 "ingredients": bridge.child_recipe.ingredients.all(),
    #             }
    #             for bridge in self.child_recipes.all()
    #         ],
    #     }

    def get_all_ingredients(self):
        return self.ingredient_requirements.all()

    def __str__(self):
        return f"{self.name}"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        "recipe", on_delete=models.CASCADE, related_name="ingredient_requirements"
    )
    ingredient = models.ForeignKey("ingredient", on_delete=models.CASCADE)
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2)


# class RecipeRequirement(models.Model):
#     parent_recipe = models.ForeignKey(
#         Recipe, related_name="child_recipes", on_delete=models.CASCADE
#     )
#     child_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
#     quantity_needed = models.DecimalField(max_digits=10, decimal_places=2)
