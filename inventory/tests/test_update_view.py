from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Ingredient


class IngredientUpdateViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(
            user=self.user, name="Egg", stock_qty=10, price=20
        )
        self.url = reverse(
            "inventory:ingredient_update", kwargs={"pk": self.ingredient.pk}
        )

    def test_update_view_displays_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/ingredient_form.html")

    def test_update_view_valid_post_updates_ingredient(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "Egg",
                "unit": "g",
                "stock_qty": 20,
                "price": 20,
            },
        )
        self.ingredient.refresh_from_db()
        self.assertRedirects(response, reverse("inventory:ingredient_list"))
        self.assertEqual(self.ingredient.stock_qty, 20)

    def test_update_view_invalid_post_does_not_update_ingredient(self):
        original_name = self.ingredient.name
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "",
                "unit": "g",
                "stock_qty": 10,
                "price": 20,
            },
        )
        self.ingredient.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.ingredient.name, original_name)

    def test_update_view_successful_post_redirects(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "Butter",
                "unit": "g",
                "stock_qty": 20,
                "price": 12,
            },
        )

        self.assertRedirects(response, reverse("inventory:ingredient_list"))
