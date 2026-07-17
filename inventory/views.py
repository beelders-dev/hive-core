from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from django.views.generic import View
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.urls import reverse_lazy

from .models import Ingredient, IngredientPurchase, PurchaseAdjustment
from .forms import IngredientForm, IngredientPurchaseForm, PurchaseAdjustmentForm


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredient/list.html"
    context_object_name = "ingredient_list"

    def get_queryset(self):
        qs = Ingredient.objects.filter(user=self.request.user)
        q = self.request.GET.get("q", "").strip()

        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["show_add_button"] = (
            self.request.GET.get("use_case") == "recipe_add_form"
        )

        return context

    def get_template_names(self):

        if "HX-Request" in self.request.headers:
            return ["inventory/ingredient/partials/_ingredient_results.html"]

        return [self.template_name]


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient/form.html"
    form_class = IngredientForm
    success_url = reverse_lazy("inventory:ingredient_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return render(
            self.request,
            "inventory/ingredient/partials/_create_success_oob.html",
            {"ingredient_list": Ingredient.objects.filter(user=self.request.user)},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["action_url"] = reverse("inventory:ingredient_create")

        return context


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient/form.html"
    form_class = IngredientForm

    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        return render(
            self.request, "inventory/ingredient/partials/_edit_success_oob.html"
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["action_url"] = reverse(
            "inventory:ingredient_update", kwargs={"pk": self.kwargs["pk"]}
        )

        return context


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient/delete.html"
    success_url = reverse_lazy("inventory:ingredient_list")

    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient"] = self.get_object()

        return context


class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    template_name = "inventory/ingredient/detail.html"
    context_object_name = "ingredient"

    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user)


class PurchaseListView(LoginRequiredMixin, ListView):
    model = IngredientPurchase
    template_name = "inventory/purchase/partials/_purchase_list.html"
    context_object_name = "purchases"


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = IngredientPurchase
    template_name = "inventory/purchase/partials/_purchase_form.html"
    success_template_name = "inventory/purchase/partials/_purchase_create_success.html"
    form_class = IngredientPurchaseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_type"] = "create"
        context["action_url"] = reverse(
            "inventory:purchase_create", kwargs={"pk": self.kwargs["pk"]}
        )

        return context

    def form_invalid(self, form):
        # response = super().form_invalid(form)
        return render(
            self.request,
            self.template_name,
            {
                "form": form,
                "ingredient": get_object_or_404(
                    Ingredient, pk=self.kwargs.pk, user=self.request.user
                ),
            },
            status=400,
        )

    def form_valid(self, form):
        ingredient = get_object_or_404(
            Ingredient, pk=self.kwargs["pk"], user=self.request.user
        )
        purchase = form.save(commit=False)
        purchase.ingredient = ingredient
        purchase.save()

        purchases = ingredient.purchases.all().order_by("purchased_at")

        return render(
            self.request,
            self.success_template_name,
            {
                "form": form,
                "ingredient": ingredient,
                "purchases": purchases,
            },
        )


class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = IngredientPurchase
    context_object_name = "ingredient_purchase"

    template_name = "inventory/purchase/purchase_detail.html"


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = IngredientPurchase
    form_class = IngredientPurchaseForm

    template_name = "inventory/purchase/partials/_edit_purchase_modal.html"

    def get_success_url(self):
        return reverse(
            "inventory:purchase",
            kwargs={"pk": self.object.pk},
        )

    def get_context_data(self, **kwargs):
        purchase = self.get_object()

        context = super().get_context_data(**kwargs)

        context["action_url"] = reverse(
            "inventory:purchase_edit",
            kwargs={"pk": purchase.pk},
        )

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)

        # Additional logic maybe put here in the future :-)

        self.object.save()

        if self.request.headers.get("HX-Request"):
            response = HttpResponse(
                '<div id="modal-root" hx-swap-oob="innerHTML"></div>'
            )
            response["HX-Refresh"] = "true"
            return response

        return HttpResponseRedirect(self.get_success_url())


class PurchaseAdjustmentListView(LoginRequiredMixin, View):

    template_name = "inventory/purchase/partials/_adjustment_list.html"

    def get(self, request, pk):

        purchase = get_object_or_404(IngredientPurchase, pk=pk)

        adjustments = purchase.adjustments.all()

        return render(
            request,
            self.template_name,
            {"adjustment_list": adjustments},
        )


class PurchaseAdjustmentCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseAdjustment
    template_name = "inventory/purchase/partials/_adjustment_create_modal.html"
    form_class = PurchaseAdjustmentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["purchase"] = get_object_or_404(
            IngredientPurchase, pk=self.kwargs["pk"]
        )

        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        purchase = get_object_or_404(
            IngredientPurchase,
            pk=self.kwargs["pk"],
        )

        new_qty = (
            self.object.qty_adjustment + purchase.get_total_stocks_plus_adjustments
        )

        if new_qty < 0:

            form.add_error("qty_adjustment", "Stock quantity cannot be negative.")
            return self.form_invalid(form)

        self.object.purchase = purchase
        self.object.save()

        return render(
            self.request,
            "inventory/purchase/partials/_adjustment_create_oob.html",
            {
                "adjustment_list": self.object.purchase.adjustments.all(),
            },
        )
