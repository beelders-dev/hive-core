from django.test import TestCase
from django.urls import reverse
from .models import Product

# Create your tests here.


class ProductTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.product = Product.objects.create(
            name="Dubai Chewy Mochi",
            price=120.00,
            stock=100,
        )

    def test_product_list_page(self):
        response = self.client.get(reverse("product_list"))
        self.assertEqual(response.status_code, 200)

    def test_product_listing(self):
        self.assertEqual(self.product.name, "Dubai Chewy Mochi")
        self.assertEqual(self.product.price, 120.00)
        self.assertEqual(self.product.stock, 100)

    def test_template_used(self):
        response = self.client.get(reverse("product_list"))
        self.assertTemplateUsed(response, "products/product_list.html")
