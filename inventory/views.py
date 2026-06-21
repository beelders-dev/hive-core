from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.urls import reverse_lazy

from .models import Ingredient
from .forms import IngredientForm

# Create your views here.


class IngredientListView(LoginRequiredMixin, ListView):
    model = Ingredient
    template_name = "inventory/ingredient_list.html"
    context_object_name = "ingredient_list"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "")

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
            return ["inventory/partials/_ingredient_results.html"]

        return [self.template_name]


class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_form.html"
    form_class = IngredientForm
    success_url = reverse_lazy("inventory:ingredient_list")


class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_form.html"
    form_class = IngredientForm
    success_url = reverse_lazy("inventory:ingredient_list")


class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete.html"
    success_url = reverse_lazy("inventory:ingredient_list")


class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = "inventory/ingredient_detail.html"
    context_object_name = "ingredient"
