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
        name="production_dashboard",
    ),
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
        "recipes/<uuid:pk>/ingredients/",
        RecipeFormIngredientListView.as_view(),
        name="ingredients",
    ),
    path(
        "recipes/ingredients/",
        RecipeFormIngredientListView.as_view(),
        name="ingredients",
    ),
    path(
        "recipes/<uuid:pk>/add-ingredient/",
        AddIngredientView.as_view(),
        name="add_ingredient",
    ),
    path(
        "recipes/<uuid:pk>/create-batch",
        CreateBatchView.as_view(),
        name="create_batch",
    ),
    path(
        "batches/<uuid:pk>/",
        BatchDetailView.as_view(),
        name="batch",
    ),
    path(
        "batches/<uuid:pk>/link-products",
        LinkProductsView.as_view(),
        name="link_products",
    ),
    path(
        "batches/<uuid:pk>/complete",
        CompleteProductionView.as_view(),
        name="complete",
    ),
    path(
        "batches/<uuid:pk>/produce",
        StartProductionView.as_view(),
        name="produce",
    ),
    path(
        "batches/<uuid:pk>/cancel",
        CancelProductionView.as_view(),
        name="cancel",
    ),
]
