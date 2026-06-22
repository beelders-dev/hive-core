from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Ingredient


class IngredientDetailViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(
            user=self.user, name="Egg", stock_qty=10, price=20
        )
        self.url = reverse(
            "inventory:ingredient",
            kwargs={
                "pk": self.ingredient.pk,
            },
        )
        self.response = self.client.get(self.url)

    def test_detail_view_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "inventory/ingredient_detail.html")

    def test_detail_view_displays_correctly(self):
        self.assertEqual(self.response.context["ingredient"], self.ingredient)
