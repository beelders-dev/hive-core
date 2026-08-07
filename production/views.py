from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.utils import timezone
from datetime import date
from django.views import View
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from inventory.models import Ingredient

from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
    ListView,
)
from .forms import BatchCancellationForm, RecipeForm
from .models import Recipe, ProductionBatch
from .services import RecipeService, ProductionService


class RecipeFormIngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredient/partials/_results_list.html"

    def get_queryset(self):
        q = self.request.GET.get("q", "")
        selected_ingredients = self.request.GET.getlist("ingredient_ids")
        qs = Ingredient.objects.filter(user=self.request.user).exclude(
            pk__in=selected_ingredients
        )
        if q:
            qs = qs.filter(name__icontains=q)

        return qs


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "production/recipe/form.html"
    success_template_name = "production/recipe/oob/_create_success.html"
    form_class = RecipeForm

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.user = self.request.user

        ingredients = []
        ingredient_ids = self.request.POST.getlist("ingredient_ids")
        quantities = self.request.POST.getlist("quantities")

        for ingredient_id, quantity in zip(ingredient_ids, quantities):
            ingredients.append(
                {
                    "ingredient_id": ingredient_id,
                    "quantity": quantity,
                }
            )
        try:

            RecipeService.create(
                recipe=recipe,
                ingredients=ingredients,
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
            "production/recipe/oob/_create_success.html",
            {
                "message": "Recipe created successfully.",
                "type": "success",
                "form": RecipeForm(),
                "ingredient_list": Ingredient.objects.filter(user=self.request.user),
            },
        )

    def form_invalid(self, form):
        return render(
            self.request,
            "production/recipe/oob/_form_error.html",
            {"form": form},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["results_url"] = reverse(
            "production:ingredients",
        )
        context["form_action_url"] = reverse("production:recipe_create")

        return context


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = "production/recipe/form.html"
    form_class = RecipeForm

    def form_valid(self, form):
        recipe = form.save(commit=False)

        ingredients = []
        ingredient_ids = self.request.POST.getlist("ingredient_ids")
        quantities = self.request.POST.getlist("quantities")
        for ingredient_id, quantity in zip(ingredient_ids, quantities):
            ingredients.append(
                {
                    "ingredient_id": ingredient_id,
                    "quantity": quantity,
                }
            )
        try:
            RecipeService.update(
                recipe=recipe,
                ingredients=ingredients,
            )

        except ValidationError as e:
            message = e.args[0]

            return render(
                self.request,
                "components/toast/_toast_oob.html",
                {
                    "message": str(message),
                    "type": "error",
                },
            )

        return render(
            self.request,
            "production/recipe/oob/_update_success.html",
            {
                "message": "Recipe updated successfully.",
                "type": "success",
                "recipe_ingredients": recipe.get_all_ingredients(),
            },
        )

    def form_invalid(self, form):
        return render(
            self.request,
            "production/recipe/oob/_form_error.html",
            {"form": form},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe_ingredients"] = self.get_object().get_all_ingredients()

        context["results_url"] = reverse(
            "production:ingredients",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        context["form_action_url"] = reverse(
            "production:recipe_edit",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        return context


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
    success_url = reverse_lazy("production:index")


class AddIngredientView(LoginRequiredMixin, View):

    def post(self, request, pk):

        selected_ingredients = self.request.POST.getlist("ingredient_ids")
        selected_ingredients.append(str(pk))
        qs = Ingredient.objects.filter(user=self.request.user).exclude(
            pk__in=selected_ingredients
        )

        return render(
            self.request,
            "production/recipe/oob/add_ingredient.html",
            {
                "ingredient_list": qs,
                "ingredient": get_object_or_404(
                    Ingredient, user=self.request.user, pk=pk
                ),
            },
        )


class RemoveIngredientView(LoginRequiredMixin, View):
    def post(self, request, pk):

        selected_ingredients = self.request.POST.getlist("ingredient_ids")
        selected_ingredients.remove(str(pk))
        qs = Ingredient.objects.filter(user=self.request.user).exclude(
            pk__in=selected_ingredients
        )

        return render(
            self.request,
            "production/recipe/oob/remove_ingredient.html",
            {"ingredient_list": qs},
        )


class CreateBatchView(LoginRequiredMixin, View):

    def post(self, request, pk):

        recipe = get_object_or_404(Recipe, user=request.user, pk=pk)

        try:
            ProductionService.produce_recipe(recipe)

        except ValidationError as e:
            print(e.message)
            return render(
                request,
                "components/toast/_toast_oob.html",
                {
                    "message": "Batch cannot be created:" + str(e.message),
                    "type": "error",
                },
            )

        return render(
            request,
            "production/batch/oob/_create_success.html",
            {
                "recipe": recipe,
                "message": "Batch created.",
                "type": "success",
            },
        )


class ProductionDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "production/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["batches"] = ProductionBatch.objects.filter(
            user=self.request.user
        ).order_by("-created_at")

        context["recipes"] = Recipe.objects.filter(user=self.request.user).order_by(
            "name"
        )
        context["completed_today"] = (
            ProductionBatch.objects.filter(user=self.request.user)
            .filter(completed_at__date=timezone.localdate())
            .count()
        )

        return context


class BatchDetailView(LoginRequiredMixin, DetailView):
    model = ProductionBatch
    context_object_name = "batch"
    template_name = "production/batch/detail.html"


class LinkProductsView(LoginRequiredMixin, View):
    pass


class CompleteProductionView(LoginRequiredMixin, View):
    template_name = "production/batch/oob/_action_btn_reload.html"

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
    template_name = "production/batch/oob/_action_btn_reload.html"

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
    template_name = "production/batch/partials/_cancel_modal_form.html"

    def get(self, request, pk):
        prod_batch = get_object_or_404(
            ProductionBatch,
            user=request.user,
            pk=pk,
        )
        form = BatchCancellationForm()

        return render(
            request,
            self.template_name,
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
            "production/batch/oob/_action_btn_reload.html",
            {"batch": prod_batch, "form": form},
        )
