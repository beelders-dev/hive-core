from django.urls import path
from django.views.generic import TemplateView
from .views import (
    RecipeDetailView,
    RecipeUpdateView,
    RemoveIngredientView,
    AddIngredientView,
    RecipeCreateView,
    RecipeDeleteView,
    CreateBatchView,
    ProductionDashboardView,
    BatchDetailView,
    LinkProductsView,
    CompleteProductionView,
    StartProductionView,
    CancelProductionView,
    RecipeFormIngredientListView,
)

app_name = "production"

urlpatterns = [
    path(
        "",
        ProductionDashboardView.as_view(),
        name="index",
    ),
    path("recipe/create/", RecipeCreateView.as_view(), name="recipe_create"),
    path("recipe/<uuid:pk>/", RecipeDetailView.as_view(), name="recipe"),
    path("recipe/<uuid:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
    path("recipe/<uuid:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path(
        "recipe/<uuid:pk>/ingredients/",
        RecipeFormIngredientListView.as_view(),
        name="ingredients",
    ),
    path(
        "recipe/ingredients/",
        RecipeFormIngredientListView.as_view(),
        name="ingredients",
    ),
    path(
        "recipe/<uuid:pk>/ingredient/add",
        AddIngredientView.as_view(),
        name="add_ingredient",
    ),
    path(
        "recipe/<uuid:pk>/ingredient/remove/",
        RemoveIngredientView.as_view(),
        name="remove_ingredient",
    ),
    path(
        "recipe/<uuid:pk>/batch/create/",
        CreateBatchView.as_view(),
        name="create_batch",
    ),
    path(
        "recipe/<uuid:pk>/batch/",
        BatchDetailView.as_view(),
        name="batch",
    ),
    path(
        "recipe/<uuid:pk>/batch/link-products/",
        LinkProductsView.as_view(),
        name="link_products",
    ),
    path(
        "recipe/<uuid:pk>/batch/complete/",
        CompleteProductionView.as_view(),
        name="complete",
    ),
    path(
        "recipe/<uuid:pk>/batch/produce/",
        StartProductionView.as_view(),
        name="produce",
    ),
    path(
        "recipe/<uuid:pk>/batch/cancel/",
        CancelProductionView.as_view(),
        name="cancel",
    ),
]
