from django.urls import path
from django.views.generic import TemplateView
from .views import (
    RecipeDetailView,
    RecipeListView,
    RecipeCreateView,
    RecipeDeleteView,
    RecipeUpdateView,
    RecipeIngredientAddView,
    SelectedIngredientsView,
    ClearDraftIngredientsView,
    RecipeIngredientRemoveView,
    RecipeIngredientQuantityUpdateView,
)

app_name = "production"

urlpatterns = [
    path("", TemplateView.as_view(template_name="temp.html")),
    path("recipes/", RecipeListView.as_view(), name="recipe_list"),
    path(
        "recipes/add/", RecipeCreateView.as_view(), name="recipe_add"
    ),  # endpoint name will need to change
    path("recipes/<uuid:pk>/", RecipeDetailView.as_view(), name="recipe"),
    path(
        "recipes/add/selected-ingredients",
        SelectedIngredientsView.as_view(),
        name="selected_ingredients",
    ),
    path(
        "recipes/<uuid:pk>/add/",
        RecipeIngredientAddView.as_view(),
        name="recipe_ingredient_add",
    ),
    path(
        "recipes/add/clear-draft",
        ClearDraftIngredientsView.as_view(),
        name="recipe_ingredient_clear",
    ),
    path(
        "recipes/<uuid:pk>/remove/",
        RecipeIngredientRemoveView.as_view(),
        name="recipe_ingredient_remove",
    ),
    path(
        "recipes/<uuid:pk>/update-quantity",
        RecipeIngredientQuantityUpdateView.as_view(),
        name="recipe_ingredient_quantity_update",
    ),
    path("recipes/<uuid:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path("recipes/<uuid:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
]
