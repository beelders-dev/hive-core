from django.views import View
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse

from .services import RecipeBuilder
from inventory.models import Ingredient

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import Recipe

SELECTED_INGEREDIENT_TABLE_TEMPLATE = "production/recipe/partials/selected_ingredients_table/_selected_ingredients_table.html"


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


class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = "production/recipe/recipe_add.html"
    fields = ["name", "ingredients"]


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "production/recipe/recipe_delete.html"
    success_url = reverse_lazy("production:recipe_list")


class RecipeCreateView(CreateView):
    model = Recipe
    fields = ["name"]
    template_name = "production/recipe/recipe_form.html"
    success_url = reverse_lazy("production:recipe_list")

    def form_valid(self, form):

        response = super().form_valid(form)

        builder = RecipeBuilder(self.request.session)

        builder.create_recipe_ingredients(recipe=self.object)

        builder.clear()

        return response


class RecipeIngredientAddView(
    View
):  # Change function name later to a more appropriate one

    def post(self, request, pk):

        builder = RecipeBuilder(request.session)

        builder.add(pk)

        return render(
            request,
            SELECTED_INGEREDIENT_TABLE_TEMPLATE,
            {"ingredients": builder.get_ingredients()},
        )


class SelectedIngredientsView(View):

    def get(self, request):

        selected = request.session.get("selected_ingredients", {})

        ingredients = Ingredient.objects.filter(id__in=selected.keys())

        for ingredient in ingredients:

            ingredient.quantity = selected.get(str(ingredient.id), {}).get(
                "quantity", ""
            )

        return render(
            request,
            SELECTED_INGEREDIENT_TABLE_TEMPLATE,
            {"ingredients": ingredients},
        )


class ClearDraftIngredientsView(View):

    def post(self, request):

        builder = RecipeBuilder(request.session)

        builder.clear()

        return render(
            request,
            SELECTED_INGEREDIENT_TABLE_TEMPLATE,
            {"selected_ingredients": {}},
        )


class RecipeIngredientRemoveView(View):

    def post(self, request, pk):

        builder = RecipeBuilder(request.session)

        selected = builder.get_selected()

        request.session[builder.SESSION_KEY] = selected
        request.session.modified = True

        builder.remove(pk)

        return render(
            request,
            SELECTED_INGEREDIENT_TABLE_TEMPLATE,
            {"ingredients": builder.get_ingredients()},
        )


class RecipeIngredientQuantityUpdateView(View):

    def post(self, request, pk):

        builder = RecipeBuilder(request.session)

        quantity = request.POST.get(f"quantity_{pk}")

        selected = builder.get_selected()

        ingredient_id = str(pk)

        if ingredient_id in selected:
            selected[ingredient_id]["quantity"] = quantity

        request.session[builder.SESSION_KEY] = selected

        return HttpResponse(status=204)
