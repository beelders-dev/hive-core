from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView

from .models import Product
from .forms import ProductCreateForm

# Create your views here.


class ProductListView(ListView):
    model = Product
    context_object_name = "product_list"
    template_name = "products/product_list.html"


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductCreateForm
    template_name = "products/product_create.html"
