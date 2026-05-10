from django import forms
from extra_views import InlineFormSetFactory
from .models import RecipeIngredient


class IngredientInline(InlineFormSetFactory):
    model = RecipeIngredient
    fields = ["ingredient", "quantity_needed"]
    factory_kwargs = {"extra": 5}
