from django.urls import path

from .views import IngredientListView, RecipeListView, RecipeDetailView

urlpatterns = [
    path("", IngredientListView.as_view(), name="ingredient_list"),
    path("recipes/", RecipeListView.as_view(), name="recipe_list"),
    path("recipes/<uuid:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
]
