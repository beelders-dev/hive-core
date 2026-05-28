from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.urls import reverse_lazy

from .models import Ingredient

# Create your views here.


class IngredientListView(ListView):
    model = Ingredient
    template_name = "inventory/ingredient_list.html"
    context_object_name = "ingredient_list"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "")

        if q:
            qs = qs.filter(name__icontains=q)
        return qs

    def get_template_names(self):

        if "HX-Request" in self.request.headers:
            use_case = self.request.GET.get("use_case")

            if use_case == "recipe_add_form":
                return ["inventory/partials/_ingredient_results.html"]

        return [self.template_name]


class IngredientCreateView(CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_form.html"
    fields = ["name", "stock_qty", "price"]
    success_url = reverse_lazy("inventory:ingredient_list")


class IngredientUpdateView(UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_form.html"
    fields = ["name", "stock_qty", "price"]
    success_url = reverse_lazy("inventory:ingredient_list")


class IngredientDeleteView(DeleteView):
    model = Ingredient
    template_name = "inventory/ingredient_delete.html"
    success_url = reverse_lazy("inventory:ingredient_list")


class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = "inventory/ingredient_detail.html"
    context_object_name = "ingredient"
