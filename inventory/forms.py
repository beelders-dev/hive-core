from django import forms
from .models import Ingredient, IngredientPurchase


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = [
            "name",
            "unit",
            "low_stock_threshold",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                }
            ),
            "unit": forms.Select(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                }
            ),
            "low_stock_threshold": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/20",
                }
            ),
        }

        labels = {
            "low_stock_threshold": "Low stock alert",
        }


class IngredientPurchaseForm(forms.ModelForm):
    class Meta:
        model = IngredientPurchase

        fields = [
            "purchased_at",
            "exp_date",
            "qty_purchased",
            "total_cost",
        ]

        widgets = {
            "purchased_at": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": (
                        "w-full rounded-lg border border-slate-300 "
                        "px-3 py-2 text-sm focus:border-blue-500 "
                        "focus:outline-none focus:ring-2 "
                        "focus:ring-blue-500/20"
                    ),
                }
            ),
            "exp_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": (
                        "w-full rounded-lg border border-slate-300 "
                        "px-3 py-2 text-sm focus:border-blue-500 "
                        "focus:outline-none focus:ring-2 "
                        "focus:ring-blue-500/20"
                    ),
                }
            ),
            "qty_purchased": forms.NumberInput(
                attrs={
                    "step": "0.1",
                    "min": "0.1",
                    "class": (
                        "w-full rounded-lg border border-slate-300 "
                        "px-3 py-2 text-sm focus:border-blue-500 "
                        "focus:outline-none focus:ring-2 "
                        "focus:ring-blue-500/20"
                    ),
                }
            ),
            "total_cost": forms.NumberInput(
                attrs={
                    "step": "0.01",
                    "min": "0.01",
                    "class": (
                        "w-full rounded-lg border border-slate-300 "
                        "px-3 py-2 text-sm focus:border-blue-500 "
                        "focus:outline-none focus:ring-2 "
                        "focus:ring-blue-500/20"
                    ),
                }
            ),
        }

        labels = {
            "purchased_at": "Purchase Date",
            "exp_date": "Expiration Date",
            "qty_purchased": "Quantity Purchased",
            "total_cost": "Total Cost",
        }

        help_texts = {
            "exp_date": "Optional",
        }
