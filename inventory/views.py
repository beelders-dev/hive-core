from django.views.generic import ListView

from .models import Ingredient

# Create your views here.


class IngredientListView(ListView):
    model = Ingredient
    template_name = "inventory/ingredient_list.html"
    context_object_name = "ingredient_list"
