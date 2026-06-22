from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Ingredient


class IngredientCreateViewTests(TestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(
            username="mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("inventory:ingredient_add")

    def test_create_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "inventory/ingredient_form.html")

    def test_create_view_valid_post_creates_ingredient(self):
        self.client.post(
            self.url,
            {
                "name": "Butter",
                "stock_qty": 20,
                "unit": "g",
                "price": 15,
            },
        )
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_create_view_invalid_post_does_not_create_ingredient(self):
        response = self.client.post(
            self.url,
            {
                "name": "",
                "stock_qty": 20,
                "unit": "g",
                "price": 15,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_create_view_successful_post_redirects(self):
        response = self.client.post(
            self.url,
            {
                "name": "Butter",
                "stock_qty": 20,
                "unit": "g",
                "price": 12,
            },
        )

        self.assertRedirects(response, reverse("inventory:ingredient_list"))
