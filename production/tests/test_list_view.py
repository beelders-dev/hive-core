from django.test import TestCase
from django.urls import reverse


from ..models import Recipe
from inventory.models import Ingredient


class ListViewTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Cocoa Powder")

    def test_recipe_list_view_loads_correctly(self):
        response = self.client.get(reverse("production:recipe_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/recipe_list.html")
