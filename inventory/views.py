from django.views.generic import ListView, CreateView

from .models import Ingredient

# Create your views here.


class IngredientListView(ListView):
    model = Ingredient
    template_name = "inventory/ingredient_list.html"
    context_object_name = "ingredient_list"


class IngredientCreateView(CreateView):
    model = Ingredient
    template_name = "inventory/ingredient_add.html"
