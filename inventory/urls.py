from django.urls import path

from .views import IngredientListView, IngredientCreateView

app_name = "inventory"

urlpatterns = [
    path("", IngredientListView.as_view(), name="ingredient_list"),
    path("add/", IngredientCreateView.as_view(), name="add_ingredient"),
]
