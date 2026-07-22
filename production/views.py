from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.utils import timezone
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from inventory.models import Ingredient

from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
)
from .forms import BatchCancellationForm, RecipeForm
from .models import Recipe, ProductionBatch
from .services import RecipeService, ProductionService

SELECTED_INGREDIENT_TABLE_TEMPLATE = "production/recipe/partials/selected_ingredients_table/_selected_ingredients_table.html"


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "production/recipe/form.html"
    form_class = RecipeForm

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user
        recipe.save()

        ingredients = []
        for ingredient_id in self.request.POST.getlist("ingredient_ids"):
            ingredient_id = ingredient_id.strip()
            if ingredient_id:
                ingredients.append(
                    {
                        "ingredient_id": ingredient_id,
                        "quantity": self.request.POST.get(f"quantity_{ingredient_id}"),
                    }
                )
        try:
            RecipeService.create_recipe(
                recipe=recipe,
                ingredients=ingredients,
            )

        except ValidationError as e:
            print(e)
            message = e.args[0]
            return render(
                self.request,
                "components/toast/_toast_oob.html",
                {
                    "message": str(message),
                    "type": "error",
                    "form": form,
                },
            )

        return render(
            self.request,
            "production/recipe/partials/_recipe_create_success.html",
            {
                "message": "Recipe created successfully.",
                "type": "success",
                "form": RecipeForm(),
            },
        )


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = "production/recipe/form.html"
    form_class = RecipeForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe_ingredients"] = self.get_object().get_all_ingredients()
        return context

    def form_valid(self, form):
        recipe = form.save()

        ingredients = []
        for ingredient_id in self.request.POST.getlist("ingredient_ids"):
            ingredient_id = ingredient_id.strip()
            ingredients.append(
                {
                    "ingredient_id": ingredient_id,
                    "quantity": self.request.POST.get(f"quantity_{ingredient_id}"),
                }
            )
        try:
            RecipeService.update_recipe(
                recipe=recipe,
                new_ingredients=ingredients,
            )

        except ValidationError as e:
            message = e.args[0]
            return render(
                self.request,
                "components/toast/_toast_oob.html",
                {
                    "message": str(message),
                    "type": "error",
                    "form": form,
                },
            )

        return render(
            self.request,
            "production/recipe/partials/_recipe_update_success.html",
            {
                "message": "Recipe updated successfully.",
                "type": "success",
                "form": form,
                "recipe_ingredients": recipe.get_all_ingredients(),
            },
        )


class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = "production/recipe/detail.html"
    context_object_name = "recipe"

    def get_queryset(self):
        return Recipe.objects.prefetch_related(
            "ingredient_requirements__ingredient",
        )


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "production/recipe/delete.html"
    success_url = reverse_lazy("production:production_dashboard")


class RemoveIngredientView(LoginRequiredMixin, View):

    def post(self, request, pk):

        return HttpResponse("")


class AddIngredientView(LoginRequiredMixin, View):

    def post(self, request, pk):

        ingredient = get_object_or_404(Ingredient, user=self.request.user, pk=pk)

        existing_ids = request.POST.getlist("ingredient_ids")

        if str(pk) in existing_ids:
            return HttpResponse("")

        return render(
            request,
            "production/recipe/partials/selected_ingredients/_row.html",
            {"ingredient": ingredient},
        )


class CreateBatchView(LoginRequiredMixin, View):

    def post(self, request, pk):

        recipe = get_object_or_404(Recipe, user=request.user, pk=pk)

        try:
            ProductionService.produce_recipe(recipe)

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
    template_name = "production/batch/batch.html"


class LinkProductsView(LoginRequiredMixin, View):
    pass


class CompleteProductionView(LoginRequiredMixin, View):
    template_name = "production/batch/partials/_action_btn_reload_oob.html"

    def post(self, request, pk):
        prod_batch = get_object_or_404(
            ProductionBatch,
            user=request.user,
            pk=pk,
        )

        prod_batch.status = ProductionBatch.Status.COMPLETE
        prod_batch.completed_at = timezone.now()
        prod_batch.save()

        return render(
            request,
            self.template_name,
            {"batch": prod_batch},
        )


class StartProductionView(LoginRequiredMixin, View):
    template_name = "production/batch/partials/_action_btn_reload_oob.html"

    def post(self, request, pk):
        prod_batch = get_object_or_404(
            ProductionBatch,
            user=request.user,
            pk=pk,
        )

        prod_batch.status = ProductionBatch.Status.IN_PROGRESS
        prod_batch.started_at = timezone.now()
        prod_batch.save()

        return render(
            request,
            self.template_name,
            {"batch": prod_batch},
        )


class CancelProductionView(LoginRequiredMixin, View):
    template_name = "production/batch/partials/_cancel_modal.html"

    def get(self, request, pk):
        prod_batch = get_object_or_404(
            ProductionBatch,
            user=request.user,
            pk=pk,
        )
        form = BatchCancellationForm()

        return render(
            request,
            "production/batch/partials/_cancel_modal_form.html",
            {"form": form, "batch": prod_batch},
        )

    def post(self, request, pk):
        prod_batch = get_object_or_404(
            ProductionBatch,
            user=request.user,
            pk=pk,
        )

        if prod_batch.status != ProductionBatch.Status.IN_PROGRESS:
            for batch_ingredient in prod_batch.batch_ingredients.all():
                try:
                    ProductionService.reinstate(batch_ingredient, prod_batch.batch_qty)
                except ValidationError as e:
                    print("Error: ", e.message)

        form = BatchCancellationForm(request.POST, instance=prod_batch)

        if form.is_valid():
            prod_batch = form.save(commit=False)
            prod_batch.status = ProductionBatch.Status.CANCELLED
            prod_batch.cancelled_at = timezone.now()
            prod_batch.save()

        return render(
            request,
            "production/batch/partials/_action_btn_reload_oob.html",
            {"batch": prod_batch, "form": form},
        )
