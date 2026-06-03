from django.views import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse


from .services.recipe_builder import RecipeBuilder
from .services.recipe_service import RecipeService


from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
)
from .models import Recipe

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


class RecipeUpdateView(UpdateView):
    model = Recipe
    template_name = "production/recipe/recipe_add.html"
    fields = ["name", "ingredients"]


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = "production/recipe/recipe_delete.html"
    success_url = reverse_lazy("production:recipe_list")


class RecipeCreateView(View):

    template_name = "production/recipe/recipe_form.html"

    def post(self, request):
        service = RecipeService(request.session)
        service.create_recipe()
        return redirect("production:recipe_list")

    def get(self, request):
        builder = RecipeBuilder(request.session)

        context = {
            "recipe_name": builder.get_name(),
            "ingredients": builder.get_ingredients(),
        }

        return render(request, self.template_name, context)


class DraftIngredientAddView(View):

    def post(self, request, pk):
        builder = RecipeBuilder(request.session)
        builder.add(pk)

        return render(
            request,
            SELECTED_INGREDIENT_TABLE_TEMPLATE,
            {"ingredients": builder.get_ingredients()},
        )


class DraftIngredientListView(View):

    def get(self, request):
        builder = RecipeBuilder(request.session)

        return render(
            request,
            SELECTED_INGREDIENT_TABLE_TEMPLATE,
            {"ingredients": builder.get_ingredients()},
        )


class DraftIngredientClearView(View):

    def post(self, request):
        builder = RecipeBuilder(request.session)
        builder.clear()

        return render(
            request,
            SELECTED_INGREDIENT_TABLE_TEMPLATE,
            {"ingredients": builder.get_ingredients()},
        )


class DraftIngredientRemoveView(View):

    def post(self, request, pk):
        builder = RecipeBuilder(request.session)
        builder.remove(pk)

        return render(
            request,
            SELECTED_INGREDIENT_TABLE_TEMPLATE,
            {"ingredients": builder.get_ingredients()},
        )


class DraftIngredientQuantityUpdateView(View):

    def post(self, request, pk):
        builder = RecipeBuilder(request.session)
        quantity = request.POST.get(f"quantity_{pk}")
        builder.update_quantity(pk, quantity)

        return HttpResponse(status=204)


class DraftRecipeNameUpdateView(View):

    def post(self, request):
        builder = RecipeBuilder(request.session)
        name = request.POST.get("name")
        builder.update_name(name)

        return HttpResponse(status=204)


class DraftRecipeNameView(View):

    def get(self, request):
        builder = RecipeBuilder(request.session)

        return render(
            request,
            "production/recipe/partials/recipe_form/_recipe_name_input.html",
            {"recipe_name": builder.get_name()},
        )
