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

    def test_user_redirects_to_login_page_when_logged_out(self):

        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )
