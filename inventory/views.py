from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django.views.generic import View
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.urls import reverse_lazy

from .models import Ingredient, IngredientPurchase
from .forms import IngredientForm, IngredientPurchaseForm


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
        return super().form_valid(form)


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient/form.html"
    form_class = IngredientForm
    success_url = reverse_lazy("inventory:ingredient_list")

    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient/delete.html"
    success_url = reverse_lazy("inventory:ingredient_list")

    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user)


class IngredientDetailView(LoginRequiredMixin, DetailView):
    model = Ingredient
    template_name = "inventory/ingredient/detail.html"
    context_object_name = "ingredient"

    def get_queryset(self):
        return Ingredient.objects.filter(user=self.request.user)


class PurchaseListView(LoginRequiredMixin, View):
    template_name = "inventory/purchase/partials/_purchase_list.html"

    def get(self, request, pk):
        ingredient = get_object_or_404(
            Ingredient,
            pk=pk,
            user=request.user,
        )

        purchases = ingredient.purchases.all()

        return render(request, self.template_name, {"purchases": purchases})


class PurchaseCreateView(LoginRequiredMixin, View):

    template_name = "inventory/purchase/partials/_purchase_form.html"
    success_template_name = "inventory/purchase/partials/_purchase_create_success.html"

    def post(self, request, pk):

        ingredient = get_object_or_404(Ingredient, pk=pk, user=request.user)

        form = IngredientPurchaseForm(request.POST)

        if not form.is_valid():
            return render(
                request,
                self.template_name,
                {"form": form, "ingredient": ingredient},
                status=400,
            )

        purchase = form.save(commit=False)
        purchase.ingredient = ingredient
        purchase.save()

        purchases = ingredient.purchases.all().order_by("purchased_at")

        return render(
            request,
            self.success_template_name,
            {
                "form": form,
                "ingredient": ingredient,
                "purchases": purchases,
            },
        )

    def get(self, request, pk):
        ingredient = get_object_or_404(Ingredient, pk=pk, user=request.user)

        form = IngredientPurchaseForm()

        return render(
            request,
            self.template_name,
            {
                "form": form,
                "ingredient": ingredient,
                "action_url": reverse(
                    "inventory:purchase_create",
                    kwargs={"pk": pk},
                ),
            },
        )


class PurchaseDetailView(LoginRequiredMixin, DetailView):
    model = IngredientPurchase
    context_object_name = "ingredient_purchase"

    template_name = "inventory/purchase/purchase_detail.html"


class PurchaseUpdateView(LoginRequiredMixin, UpdateView):
    model = IngredientPurchase
    form_class = IngredientPurchaseForm

    template_name = "inventory/purchase/partials/_form_modal.html"

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
        self.object = form.save()
        if self.request.headers.get("HX-Request"):
            response = HttpResponse(
                '<div id="modal-root" hx-swap-oob="innerHTML"></div>'
            )
            response["HX-Refresh"] = "true"
            return response

        return HttpResponseRedirect(self.get_success_url())
