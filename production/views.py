from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from inventory.models import Ingredient

from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from .models import Recipe
from .services import RecipeService

SELECTED_INGREDIENT_TABLE_TEMPLATE = "production/recipe/partials/selected_ingredients_table/_selected_ingredients_table.html"


# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    template_name = "production/recipe/recipe_list.html"
    context_object_name = "recipe_list"


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "production/recipe/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            "ingredient_requirements__ingredient",
        )


class RecipeUpdateView(View):

    def get(self, request, pk):

        recipe = Recipe.objects.get(pk=pk)

        return render(
            request,
            "production/recipe/recipe_form.html",
            {"recipe": recipe, "recipe_ingredients": recipe.get_all_ingredients()},
        )

    def post(self, request, pk):

        recipe = Recipe.objects.get(pk=pk)

        new_recipe_name = request.POST.get("recipe_name")
        new_description = request.POST.get("recipe_description")

        ingredients = []

        for ingredient_id in request.POST.getlist("ingredient_ids"):
            ingredient_id = ingredient_id.strip()
            if ingredient_id:
                ingredients.append(
                    {
                        "ingredient_id": ingredient_id,
                        "quantity": request.POST.get(f"quantity_{ingredient_id}"),
                    }
                )

        service = RecipeService()

        try:
            service.update_recipe(
                recipe=recipe,
                new_recipe_name=new_recipe_name,
                new_recipe_description=new_description,
                new_ingredients=ingredients,
            )
        except ValidationError as e:
            message = next(iter(e.message_dict.values()))[0]
            return render(
                request,
                "production/recipe/partials/_message.html",
                {
                    "message": str(message),
                    "type": "error",
                },
            )

        return render(
            request,
            "production/recipe/partials/_recipe_create_success.html",
            {
                "message": "Recipe updated successfully.",
                "type": "success",
            },
        )


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "production/recipe/recipe_delete.html"
    success_url = reverse_lazy("production:recipe_list")


class RecipeCreateView(View):

    def post(self, request):

        service = RecipeService()
        ingredients = []

        for ingredient_id in request.POST.getlist("ingredient_ids"):
            ingredient_id = ingredient_id.strip()
            if ingredient_id:
                ingredients.append(
                    {
                        "ingredient_id": ingredient_id,
                        "quantity": request.POST.get(f"quantity_{ingredient_id}"),
                    }
                )

        try:
            service.create_recipe(
                recipe_name=request.POST.get("recipe_name"),
                recipe_description=request.POST.get("recipe_description"),
                ingredients=ingredients,
            )

        except ValidationError as e:

            message = next(iter(e.message_dict.values()))[0]
            return render(
                request,
                "production/recipe/partials/_message.html",
                {
                    "message": str(message),
                    "type": "error",
                },
            )

        return render(
            request,
            "production/recipe/partials/_recipe_create_success.html",
            {
                "message": "Recipe created successfully.",
                "type": "success",
            },
        )

    def get(self, request):

        return render(request, "production/recipe/recipe_form.html")


class RemoveIngredientView(View):

    def post(self, request, pk):

        return HttpResponse("")


class AddIngredientView(View):

    def post(self, request, pk):

        ingredient = get_object_or_404(Ingredient, pk=pk)

        existing_ids = request.POST.getlist("ingredient_ids")

        if str(pk) in existing_ids:
            return HttpResponse("")

        return render(
            request,
            "production/recipe/partials/selected_ingredients_table/_selected_ingredients_table_row.html",
            {"ingredient": ingredient},
        )
