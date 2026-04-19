from django.urls import path
from .views import ProductListView, ProductDetailView, ProductCreateView

urlpatterns = [
    path("<uuid:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("", ProductListView.as_view(), name="product_list"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
]
