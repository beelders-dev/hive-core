from django.urls import path
from django.views.generic import TemplateView
from .views import (
    RecipeDetailView,
    RecipeListView,
    RecipeCreateView,
    RecipeDeleteView,
    RecipeUpdateView,
    DraftIngredientAddView,
    DraftIngredientListView,
    DraftIngredientClearView,
    DraftIngredientRemoveView,
    DraftIngredientQuantityUpdateView,
    DraftRecipeNameUpdateView,
    DraftRecipeNameView,
)

app_name = "production"

urlpatterns = [
    path("", TemplateView.as_view(template_name="temp.html")),
    path("recipes/", RecipeListView.as_view(), name="recipe_list"),
    path(
        "recipes/create/", RecipeCreateView.as_view(), name="recipe_create"
    ),  # endpoint name will need to change
    path("recipes/<uuid:pk>/", RecipeDetailView.as_view(), name="recipe"),
    path(
        "recipes/draft/selected-ingredients-view",
        DraftIngredientListView.as_view(),
        name="selected_ingredients",
    ),
    path(
        "recipes/draft/<uuid:pk>/add-item/",
        DraftIngredientAddView.as_view(),
        name="add_ingredient_to_draft",
    ),
    path(
        "recipes/draft/clear-draft",
        DraftIngredientClearView.as_view(),
        name="clear_draft",
    ),
    path(
        "recipes/draft/<uuid:pk>/remove/",
        DraftIngredientRemoveView.as_view(),
        name="update_draft_remove_ingredient",
    ),
    path(
        "recipes/draft/<uuid:pk>/update-ingredient-quantity",
        DraftIngredientQuantityUpdateView.as_view(),
        name="update_draft_ingredient_quantity",
    ),
    path(
        "recipes/draft/update-recipe-name",
        DraftRecipeNameUpdateView.as_view(),
        name="update_draft_recipe_name",
    ),
    path(
        "recipes/draft/display-recipe-name",
        DraftRecipeNameView.as_view(),
        name="draft_recipe_name_view",
    ),
    path("recipes/<uuid:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path("recipes/<uuid:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
]
