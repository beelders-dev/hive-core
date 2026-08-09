from django import forms
from .models import Ingredient, IngredientPurchase, PurchaseAdjustment


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
            "unit": forms.RadioSelect(),
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


class PurchaseAdjustmentForm(forms.ModelForm):
    class Meta:
        model = PurchaseAdjustment
        fields = ["qty_adjustment", "note"]
        widgets = {
            "qty_adjustment": forms.NumberInput(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-indigo-500 focus:ring-indigo-500",
                    "placeholder": "e.g. 5 or -2",
                    "step": "0.1",
                }
            ),
            "note": forms.Textarea(
                attrs={
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-indigo-500 focus:ring-indigo-500",
                    "rows": 3,
                    "placeholder": "Reason for this adjustment...",
                }
            ),
        }
        labels = {
            "qty_adjustment": "Quantity Adjustment",
            "note": "Reason",
        }
        help_texts = {
            "qty_adjustment": "Use a positive number to add stock and a negative number to remove stock.",
        }
