from django.urls import path

from .views import (
    IngredientListView,
    IngredientCreateView,
    IngredientDetailView,
    IngredientDeleteView,
    IngredientUpdateView,
    IngredientPurchaseListView,
    IngredientPurchaseCreateView,
    IngredientPurchaseDetailView,
)

app_name = "inventory"

urlpatterns = [
    path("ingredients/", IngredientListView.as_view(), name="ingredient_list"),
    path(
        "ingredients/create/", IngredientCreateView.as_view(), name="ingredient_create"
    ),
    path("ingredients/<uuid:pk>/", IngredientDetailView.as_view(), name="ingredient"),
    path(
        "ingredients/<uuid:pk>/delete/",
        IngredientDeleteView.as_view(),
        name="ingredient_delete",
    ),
    # path("<uuid:pk>/edit/", IngredientUpdateView.as_view(), name="ingredient_update"),
    path(
        "<uuid:pk>/purchase-list/",
        IngredientPurchaseListView.as_view(),
        name="ingredient_purchase_list",
    ),
    path(
        "/<uuid:pk>/purchase-create/",
        IngredientPurchaseCreateView.as_view(),
        name="ingredient_purchase_create",
    ),
    path(
        "purchase/<uuid:pk>",
        IngredientPurchaseDetailView.as_view(),
        name="purchase",
    ),
]
