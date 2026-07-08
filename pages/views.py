from typing import Any

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from inventory.models import Ingredient, IngredientPurchase
from production.models import Recipe

# Create your views here.


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["total_ingredients"] = Ingredient.objects.filter(
            user=self.request.user
        ).count()

        context["total_recipes"] = Recipe.objects.filter(user=self.request.user).count()
        context["low_stock_count"] = sum(
            ingredient.is_low_stock
            for ingredient in Ingredient.objects.filter(user=self.request.user)
        )
        context["out_of_stock_count"] = sum(
            ingredient.is_out_of_stock
            for ingredient in Ingredient.objects.filter(user=self.request.user)
        )

        low_stock = [
            ingredient
            for ingredient in Ingredient.objects.filter(user=self.request.user)
            if ingredient.is_low_stock
        ]
        context["low_stock_ingredients"] = low_stock

        recent_recipes = [
            recipe
            for recipe in Recipe.objects.filter(user=self.request.user).order_by(
                "-created_at"
            )[:5]
            if recipe.is_recently_added
        ]

        context["recent_recipes"] = recent_recipes

        return context
