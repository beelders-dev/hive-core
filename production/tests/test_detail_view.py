from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


from ..models import Recipe
from inventory.models import Ingredient


class DetailViewTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username="Mike", password="testpass123")
        self.client.force_login(user)
        self.ingredient = Ingredient.objects.create(user=user, name="Cocoa Powder")
        self.recipe = Recipe.objects.create(name="Chocolate bar")

    def test_recipe_detail_view_loads_correctly(self):

        response = self.client.get(reverse("production:recipe", args=[self.recipe.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["recipe"], self.recipe)
        self.assertTemplateUsed(response, "production/recipe/recipe_detail.html")
