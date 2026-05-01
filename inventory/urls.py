from django.urls import path

from .views import IngredientListView

app_name = "inventory"

urlpatterns = [
    path("", IngredientListView.as_view(), name="ingredient_list"),
]
