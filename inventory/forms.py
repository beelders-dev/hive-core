from django import forms
from .models import Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "name",
            "stock_qty",
            "unit",
            "price",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                }
            ),
            "stock_qty": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                }
            ),
        }
