from django.urls import path

from .views import (
    IngredientListView,
    IngredientCreateView,
    IngredientDetailView,
    IngredientDeleteView,
    IngredientUpdateView,
    PurchaseListView,
    PurchaseCreateView,
    PurchaseDetailView,
    PurchaseUpdateView,
)

app_name = "inventory"

urlpatterns = [
    path(
        "ingredients/",
        IngredientListView.as_view(),
        name="ingredient_list",
    ),
    path(
        "ingredients/create/",
        IngredientCreateView.as_view(),
        name="ingredient_create",
    ),
    path(
        "ingredients/<uuid:pk>/",
        IngredientDetailView.as_view(),
        name="ingredient",
    ),
    path(
        "ingredients/<uuid:pk>/delete/",
        IngredientDeleteView.as_view(),
        name="ingredient_delete",
    ),
    path(
        "ingredients/<uuid:pk>/edit/",
        IngredientUpdateView.as_view(),
        name="ingredient_update",
    ),
    path(
        "purchase/<uuid:pk>/purchase-list/",
        PurchaseListView.as_view(),
        name="purchase_list",
    ),
    path(
        "purchase/<uuid:pk>/purchase-create/",
        PurchaseCreateView.as_view(),
        name="purchase_create",
    ),
    path(
        "purchase/<uuid:pk>/",
        PurchaseDetailView.as_view(),
        name="purchase",
    ),
    path(
        "purchase/<uuid:pk>/edit",
        PurchaseUpdateView.as_view(),
        name="purchase_edit",
    ),
]
