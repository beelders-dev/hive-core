from django.urls import path
from django.views.generic import TemplateView
from .views import (
    RecipeDetailView,
    RecipeListView,
    RecipeCreateView,
    RecipeDeleteView,
    RecipeUpdateView,
)

app_name = "production"

urlpatterns = [
    path("", TemplateView.as_view(template_name="temp.html")),
    path("recipes/", RecipeListView.as_view(), name="recipe_list"),
    path("recipes/add", RecipeCreateView.as_view(), name="recipe_add"),
    path("recipes/<uuid:pk>/", RecipeDetailView.as_view(), name="recipe"),
    path("recipes/<uuid:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path("recipes/<uuid:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
]
