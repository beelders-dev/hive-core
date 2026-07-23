from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError

from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    TemplateView,
)
from django.urls import reverse_lazy

from .models import Ingredient, IngredientPurchase, PurchaseAdjustment
from .forms import IngredientForm, IngredientPurchaseForm, PurchaseAdjustmentForm
from .services import PurchaseAdjustmentService


class InventoryHomeView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient_list"] = Ingredient.objects.filter(user=self.request.user)
        return context


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredient/partials/_results_table.html"
    context_object_name = "ingredient_list"

    def get_queryset(self):
        qs = Ingredient.objects.filter(user=self.request.user)
        q = self.request.GET.get("q", "").strip()

        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_url"] = reverse("inventory:ingredient_list")

        return context


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient/partials/_form.html"
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
    template_name = "inventory/ingredient/partials/_form.html"
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
    success_url = reverse_lazy("inventory:index")

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
    template_name = "inventory/purchase/partials/_list.html"
    context_object_name = "purchases"

    def get_queryset(self):
        return IngredientPurchase.objects.filter(ingredient_id=self.kwargs["pk"])


class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = IngredientPurchase
    template_name = "inventory/purchase/partials/_form.html"
    success_template_name = "inventory/purchase/partials/_create_success_oob.html"
    form_class = IngredientPurchaseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_type"] = "create"
        context["action_url"] = reverse(
            "inventory:purchase_create", kwargs={"pk": self.kwargs["pk"]}
        )

        return context

    def form_invalid(self, form):

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
    context_object_name = "purchase"
    template_name = "inventory/purchase/detail.html"


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = IngredientPurchase
    form_class = IngredientPurchaseForm

    template_name = "inventory/purchase/partials/_form.html"

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

        self.object.save()

        if self.request.headers.get("HX-Request"):
            response = HttpResponse(
                '<div id="modal-root" hx-swap-oob="innerHTML"></div>'
            )
            response["HX-Refresh"] = "true"
            return response

        return HttpResponseRedirect(self.get_success_url())


class PurchaseAdjustmentListView(LoginRequiredMixin, ListView):
    model = PurchaseAdjustment
    template_name = "inventory/adjustment/partials/_list.html"
    context_object_name = "adjustment_list"


class PurchaseAdjustmentCreateView(LoginRequiredMixin, CreateView):
    model = PurchaseAdjustment
    template_name = "inventory/adjustment/partials/_form.html"
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

        qty_adjustment = form.cleaned_data["qty_adjustment"]
        note = form.cleaned_data["note"]

        try:
            PurchaseAdjustmentService.create(
                purchase=purchase,
                qty_adjustment=qty_adjustment,
                note=note,
            )

        except ValidationError as e:
            form.add_error("qty_adjustment", str(e.message))
            return self.form_invalid(form)

        return render(
            self.request,
            "inventory/adjustment/partials/_create_success_oob.html",
            {
                "adjustment_list": purchase.adjustments.all(),
                "purchase": purchase,
            },
        )
