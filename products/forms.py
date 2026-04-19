from django import forms
from .models import Product
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "stock", "price", "short_description", "full_description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        submit_label = "Update Product" if self.instance.pk else "Create Product"

        self.helper = FormHelper()
        self.helper.layout = Layout(
            "name",
            Row(
                Column("stock", css_class="form-group col-span-6"),
                Column("price", css_class="form-group col-span-6"),
                css_class="grid grid-cols-12 gap-4 w-1/2",
            ),
            "short_description",
            "full_description",
            Submit(
                "submit",
                submit_label,
                css_class="w-full mt-4 bg-amber-600 hover:bg-amber-700 text-white font-bold py-2 rounded-lg transition-colors",
            ),
        )
