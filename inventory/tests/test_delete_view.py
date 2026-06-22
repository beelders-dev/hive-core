from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Ingredient


class IngredientDeleteViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(
            user=self.user, name="Egg", stock_qty=10, price=20
        )
        self.url = reverse(
            "inventory:ingredient_delete", kwargs={"pk": self.ingredient.pk}
        )

    def test_delete_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "inventory/ingredient_delete.html")

    def test_delete_view_deletes_ingredient(self):
        self.client.post(self.url)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_delete_view_redirects_after_successful_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("inventory:ingredient_list"))
