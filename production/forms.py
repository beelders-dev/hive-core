from django import forms
from .models import ProductionBatch


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
