from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Ingredient


class IngredientListViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(
            user=self.user, name="Egg", stock_qty=10, price=20
        )
        self.ingredient = Ingredient.objects.create(name="Egg", stock_qty=10, price=20)
        self.url = reverse("inventory:ingredient_list")
        self.response = self.client.get(self.url)

    def test_list_view_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_list_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "inventory/ingredient_list.html")

    def test_list_view_displays_ingredients(self):
        ingredients = self.response.context["ingredient_list"]
        self.assertEqual(len(ingredients), 1)

    def test_list_view_does_not_display_content_when_user_logs_out(self):

        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )
