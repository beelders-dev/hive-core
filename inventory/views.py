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


class IngredientCreateView(CreateView):
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


class IngredientUpdateView(UpdateView):
    model = Ingredient
    template_name = "inventory/ingredient_form.html"
    fields = ["name", "stock_qty", "price"]
    success_url = reverse_lazy("inventory:ingredient_list")
