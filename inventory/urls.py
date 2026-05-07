from django.urls import path

from .views import (
    IngredientListView,
    IngredientCreateView,
    IngredientDetailView,
    IngredientDeleteView,
)

app_name = "inventory"

urlpatterns = [
    path("", IngredientListView.as_view(), name="ingredient_list"),
    path("add/", IngredientCreateView.as_view(), name="ingredient_add"),
    path("<uuid:pk>/", IngredientDetailView.as_view(), name="ingredient"),
    path("<uuid:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient_delete"),
]
