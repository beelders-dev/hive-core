from django import forms
from .models import Recipe, ProductionBatch


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "description"]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100",
                    "placeholder": "Enter recipe name...",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Describe the recipe, preparation notes, serving suggestions, or any additional details...",
                    "class": "w-full rounded-xl border border-slate-300 bg-white px-4 py-3 text-sm text-slate-900 shadow-sm placeholder:text-slate-400 focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-100 resize-none",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault("autocomplete", "off")

        if self.is_bound:
            for name, field in self.fields.items():
                if self.errors.get(name):
                    field.widget.attrs[
                        "class"
                    ] += " border-red-500 focus:border-red-500 focus:ring-red-100"


class BatchCancellationForm(forms.ModelForm):
    class Meta:
        model = ProductionBatch
        fields = [
            "cancellation_note",
        ]

        widgets = {
            "cancellation_note": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Enter the reason for cancellation...",
                    "class": "w-full rounded-lg border border-slate-300 px-3 py-2 focus:border-red-500 focus:ring-red-500",
                }
            ),
        }
