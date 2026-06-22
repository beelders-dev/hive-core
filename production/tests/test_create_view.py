from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Recipe
from inventory.models import Ingredient


class CreateViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.url = reverse("production:recipe_create")

    def test_recipe_create_view_loads_correctly(self):
        response = self.client.get(reverse("production:recipe_create"))

        self.assertTemplateUsed(response, "production/recipe/recipe_form.html")

    def test_recipe_create_view_creates_recipe_successfully(self):

        self.client.post(
            self.url,
            data={
                "recipe_name": "Chocolate Cake",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": 1,
            },
        )

        self.assertEqual(Recipe.objects.count(), 1)

    def test_recipe_create_view_displays_success_message(self):

        response = self.client.post(
            self.url,
            data={
                "recipe_name": "Chocolate bar",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": 1,
            },
        )
        self.assertContains(response, "Recipe created successfully.")
        self.assertEqual(Recipe.objects.count(), 1)

    def test_recipe_create_view_displays_error_message_when_name_is_blank(self):

        response = self.client.post(
            self.url,
            data={
                "recipe_name": "",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": 1,
            },
        )
        self.assertContains(response, "Recipe name cannot be blank.")
        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipe_create_view_displays_error_message_when_recipe_name_chars_exceeds_100(
        self,
    ):

        response = self.client.post(
            self.url,
            data={
                "recipe_name": "Chocolate Cake" * 101,
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": 1,
            },
        )
        self.assertContains(response, "Max characters for recipe name: 100")
        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipe_create_view_displays_error_message_for_invalid_quantity(self):

        response = self.client.post(
            reverse("production:recipe_create"),
            data={
                "recipe_name": "Chocolate cake",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": -1,
            },
        )
        self.assertContains(response, "Quantity must be greater than or equal to 0.01.")
        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipe_create_view_displays_error_message_when_no_ingredient_added(self):

        response = self.client.post(
            reverse("production:recipe_create"),
            data={
                "recipe_name": "Chocolate cake",
            },
        )
        self.assertContains(response, "Add at least 1 ingredient.")
        self.assertEqual(Recipe.objects.count(), 0)

    def test_recipe_create_view_creates_recipe_with_user(self):

        self.client.post(
            self.url,
            data={
                "recipe_name": "Chocolate Cake",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": 1,
            },
        )

        recipe = Recipe.objects.get(name="Chocolate Cake")
        self.assertEqual(recipe.user, self.user)
