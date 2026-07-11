from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.utils import timezone
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ValidationError

from inventory.models import Ingredient

from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    UpdateView,
    TemplateView,
)
from .forms import BatchCancellationForm
from .models import Recipe, ProductionBatch
from .services import RecipeService, ProductionService

SELECTED_INGREDIENT_TABLE_TEMPLATE = "production/recipe/partials/selected_ingredients_table/_selected_ingredients_table.html"


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "production/recipe/recipe_detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            "ingredient_requirements__ingredient",
        )


class RecipeUpdateView(LoginRequiredMixin, View):

    def get(self, request, pk):

        recipe = Recipe.objects.get(pk=pk)

        return render(
            request,
            "production/recipe/recipe_form.html",
            {"recipe": recipe, "recipe_ingredients": recipe.get_all_ingredients()},
        )

    def post(self, request, pk):

        recipe = Recipe.objects.get(user=self.request.user, pk=pk)
        service = RecipeService()

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
            "components/toast/_toast_oob.html",
            {
                "message": "Recipe updated successfully.",
                "type": "success",
            },
        )


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "production/recipe/recipe_delete.html"
    success_url = reverse_lazy("production:production_dashboard")


class RecipeCreateView(LoginRequiredMixin, View):

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
                user=self.request.user,
                recipe_name=request.POST.get("recipe_name"),
                recipe_description=request.POST.get("recipe_description"),
                ingredients=ingredients,
            )

        except ValidationError as e:

            message = next(iter(e.message_dict.values()))[0]
            return render(
                request,
                "components/toast/_toast_oob.html",
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

        return render(
            request,
            "production/recipe/recipe_form.html",
        )


class RemoveIngredientView(LoginRequiredMixin, View):

    def post(self, request, pk):

        return HttpResponse("")


class AddIngredientView(LoginRequiredMixin, View):

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


class CreateBatchView(LoginRequiredMixin, View):
    def post(self, request, pk):

        recipe = Recipe.objects.get(user=request.user, pk=pk)

        production = ProductionService()
        try:
            production.produce_recipe(recipe)

        except ValidationError as e:

            return render(
                request,
                "components/toast/_toast_oob.html",
                {
                    "message": "Batch cannot be created:" + str(e.message),
                    "type": "error",
                },
            )
        recipe.refresh_from_db()

        return render(
            request,
            "production/recipe/partials/_recipe_produce_message.html",
            {
                "recipe": recipe,
                "message": "Batch created.",
                "type": "success",
            },
        )


class ProductionDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "production/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["batches"] = ProductionBatch.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

        context["recipes"] = Recipe.objects.filter(user=self.request.user).order_by(
            "name"
        )
        context["produced_today"] = (
            ProductionBatch.objects.filter(user=self.request.user)
            .filter(completed_at__date=timezone.localdate())
            .count()
        )

        return context


class BatchDetailView(LoginRequiredMixin, DetailView):
    model = ProductionBatch
    context_object_name = "batch"
    template_name = "production/batch/batch_detail.html"


class LinkProductsView(LoginRequiredMixin, View):
    pass


class CompleteProductionView(LoginRequiredMixin, View):
    template_name = "production/batch/partials/_complete_production_oob.html"

    def post(self, request, pk):
        prod_batch = ProductionBatch.objects.get(user=request.user, pk=pk)

        if not prod_batch:
            raise ValueError("Object Not found.")

        prod_batch.status = ProductionBatch.Status.COMPLETE
        prod_batch.completed_at = timezone.now()
        prod_batch.save()

        return render(
            request,
            self.template_name,
            {"batch": prod_batch},
        )


class StartProductionView(LoginRequiredMixin, View):
    template_name = "production/batch/partials/_start_production_oob.html"

    def post(self, request, pk):
        prod_batch = ProductionBatch.objects.get(user=request.user, pk=pk)

        if not prod_batch:
            raise ValueError("Object Not found.")

        prod_batch.status = ProductionBatch.Status.IN_PROGRESS

        prod_batch.save()

        return render(
            request,
            self.template_name,
            {"batch": prod_batch},
        )


class CancelProductionView(LoginRequiredMixin, View):
    template_name = "production/batch/partials/_cancel_production_oob.html"

    def get(self, request, pk):
        prod_batch = ProductionBatch.objects.get(user=request.user, pk=pk)
        form = BatchCancellationForm()

        return render(
            request,
            "production/batch/partials/_cancel_modal.html",
            {"form": form, "batch": prod_batch},
        )

    def post(self, request, pk):
        prod_batch = ProductionBatch.objects.get(user=request.user, pk=pk)

        if not prod_batch:
            raise ValueError("Object Not found.")

        prod_service = ProductionService()

        if prod_batch.status != ProductionBatch.Status.IN_PROGRESS:
            for batch_ingredient in prod_batch.batch_ingredients.all():
                try:
                    prod_service.reinstate(batch_ingredient, prod_batch.batch_qty)
                except ValidationError as e:
                    print("Error: ", e.message)

        prod_batch.status = ProductionBatch.Status.CANCELLED
        prod_batch.cancelled_at = timezone.now()
        prod_batch.save()

        return HttpResponseRedirect(
            reverse_lazy("production:batch", kwargs={"pk": prod_batch.pk})
        )
