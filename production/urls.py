from django.urls import path
from django.views.generic import TemplateView
from .views import (
    RecipeDetailView,
    RecipeListView,
    RecipeUpdateView,
    RemoveIngredientView,
    AddIngredientView,
    RecipeCreateView,
    RecipeDeleteView,
    RecipeProduceView,
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
        "recipes/<uuid:pk>/remove/",
        RemoveIngredientView.as_view(),
        name="remove_ingredient",
    ),
    path("recipes/<uuid:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
    path("recipes/<uuid:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path(
        "recipes/<uuid:pk>/add-ingredient/",
        AddIngredientView.as_view(),
        name="add_ingredient",
    ),
    path(
        "recipes/<uuid:pk>/produce", RecipeProduceView.as_view(), name="recipe_produce"
    ),
]
