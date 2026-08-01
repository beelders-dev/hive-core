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
        "recipe/<uuid:pk>/batch/create",
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
