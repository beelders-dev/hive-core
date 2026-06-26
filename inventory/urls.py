from django.urls import path

from .views import (
    IngredientListView,
    IngredientCreateView,
    IngredientDetailView,
    IngredientDeleteView,
    IngredientUpdateView,
    IngredientPurchaseListView,
    IngredientPurchaseCreateView,
)

app_name = "inventory"

urlpatterns = [
    path("", IngredientListView.as_view(), name="ingredient_list"),
    path("create/", IngredientCreateView.as_view(), name="ingredient_create"),
    path("<uuid:pk>/", IngredientDetailView.as_view(), name="ingredient"),
    path("<uuid:pk>/delete/", IngredientDeleteView.as_view(), name="ingredient_delete"),
    # path("<uuid:pk>/edit/", IngredientUpdateView.as_view(), name="ingredient_update"),
    path(
        "<uuid:pk>/ingredient-purchase-list/",
        IngredientPurchaseListView.as_view(),
        name="ingredient_purchase_list",
    ),
    path(
        "<uuid:pk>/ingredient-purchase-create/",
        IngredientPurchaseCreateView.as_view(),
        name="ingredient_purchase_create",
    ),
]
