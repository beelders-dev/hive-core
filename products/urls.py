from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductDeleteView,
    ProductUpdateView,
)

app_name = "products"

urlpatterns = [
    path("<uuid:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("", ProductListView.as_view(), name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("<uuid:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path("<uuid:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
]
