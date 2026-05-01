from django.urls import path
from django.views.generic import TemplateView
from .views import RecipeDetailView, RecipeListView

urlpatterns = [
    path("", TemplateView.as_view(template_name="temp.html"), name="recipe_list"),
    path("recipe/", RecipeListView.as_view(), name="recipe_list"),
    path("recipe/<uuid:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
]
