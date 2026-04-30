from django.views.generic import ListView, DetailView

from .models import Ingredient, Recipe

# Create your views here.


class IngredientListView(ListView):
    model = Ingredient
    template_name = "inventory/ingredient_list.html"
    context_object_name = "ingredient_list"


class RecipeListView(ListView):
    model = Recipe
    template_name = "inventory/recipe/recipe_list.html"
    context_object_name = "recipe_list"


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "inventory/recipe/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            "ingredient_requirements__ingredient",
        )
