from django import forms
from .models import Product


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "stock", "price", "short_description", "full_description"]
