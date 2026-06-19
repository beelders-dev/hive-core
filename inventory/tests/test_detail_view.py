from django.test import TestCase
from django.urls import reverse

from ..models import Ingredient


class IngredientDetailViewTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Egg", stock_qty=10, price=20)
        self.url = reverse("inventory:ingredient", kwargs={"pk": self.ingredient.pk})
        self.response = self.client.get(self.url)

    def test_detail_view_returns_200(self):
        self.assertEqual(self.response.status_code, 200)

    def test_detail_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, "inventory/ingredient_detail.html")

    def test_detail_view_displays_correctly(self):
        self.assertEqual(self.response.context["ingredient"], self.ingredient)
