from django.test import TestCase
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth import get_user_model
from ..models import Recipe, RecipeIngredient
from inventory.models import Ingredient


class UpdateViewTests(TestCase):

    def setUp(self):
        user = get_user_model().objects.create(username="Mike", password="testpass123")
        self.client.force_login(user)
        self.ingredient = Ingredient.objects.create(user=user, name="Cocoa Powder")

        self.recipe = Recipe.objects.create(user=user, name="Brownies")

        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity_needed=Decimal(5.00),
        )
        self.url = reverse("production:recipe_edit", args=[self.recipe.pk])

    def test_update_view_loads_correctly(self):
        response = self.client.get(
            reverse("production:recipe_edit", args=[self.recipe.pk])
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/recipe_form.html")
        self.assertContains(response, "Brownies")

    def test_update_view_displays_success_message_correctly(self):
        response = self.client.post(
            self.url,
            data={
                "recipe_name": "Cookies",
                "ingredient_ids": [str(self.ingredient.pk)],
                f"quantity_{self.ingredient.pk}": Decimal(2.00),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Recipe updated successfully.")

    def test_update_view_displays_error_msg_when_no_ingredient_added(self):

        response = self.client.post(
            self.url,
            data={
                "recipe_name": "Cookies",
            },
        )

        self.assertContains(response, "Add at least 1 ingredient.")
