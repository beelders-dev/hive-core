from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from decimal import Decimal

from inventory.models import Ingredient
from production.models import Recipe, RecipeIngredient

from bs4 import BeautifulSoup


class RecipeFormIngredientListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.flour = Ingredient.objects.create(
            user=self.user,
            name="Flour",
        )
        self.chocolate_bar = Ingredient.objects.create(
            user=self.user,
            name="Chocolate Bar",
        )
        self.url = reverse("production:ingredients")

    def test_recipe_form_ingredient_list_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "inventory/ingredient/partials/_results_list.html"
        )

    def test_get_queryset_excludes_selected_ingredients(self):
        response = self.client.get(
            self.url,
            {
                "ingredient_ids": [str(self.flour.id)],
            },
        )

        ingredients = response.context["object_list"]

        self.assertNotIn(self.flour, ingredients)
        self.assertIn(self.chocolate_bar, ingredients)

    def test_get_queryset_filters_and_excludes_selected_ingredients(self):
        response = self.client.get(
            self.url,
            {
                "q": "flour",
                "ingredient_ids": [str(self.flour.id)],
            },
        )

        self.assertQuerySetEqual(
            response.context["object_list"],
            [],
            transform=lambda x: x,
        )

    def test_recipe_form_ingredient_list_renders_objects(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Flour")

    def test_recipe_form_ingredient_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class RecipeCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.flour = Ingredient.objects.create(
            user=self.user,
            name="Flour",
        )
        self.chocolate_bar = Ingredient.objects.create(
            user=self.user,
            name="Chocolate Bar",
        )

        self.url = reverse("production:recipe_create")

    def test_recipe_create_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "production/recipe/form.html")

    def test_recipe_create_view_loads_ingredient_list_context(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.context["results_url"],
            reverse("production:ingredients"),
        )

    def test_recipe_create_view_loads_recipe_create_context(self):
        response = self.client.get(self.url)
        self.assertEqual(
            response.context["form_action_url"],
            reverse("production:recipe_create"),
        )

    def test_recipe_create_view_renders_success_template(self):
        response = self.client.post(
            self.url,
            data={
                "name": "Chocolate Cake",
                "description": "Lorem Ipsum",
                "ingredient_ids": [str(self.flour.pk)],
                "quantities": Decimal("100"),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/oob/_create_success.html")

    def test_recipe_create_view_renders_error_template_when_name_is_blank(self):
        response = self.client.post(
            self.url,
            data={
                "name": " ",
                "description": "Lorem Ipsum",
                "ingredient_ids": [str(self.flour.pk)],
                "quantities": Decimal("100"),
            },
        )
        self.assertTemplateUsed(response, "production/recipe/oob/_form_error.html")

    def test_recipe_create_view_renders_error_toast_when_zero_ingredient(
        self,
    ):
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "Chocolate Cake",
                "description": "Lorem Ipsum",
                "ingredient_ids": [],
                "quantities": Decimal("100"),
            },
        )
        self.assertTemplateUsed(response, "components/toast/_toast_oob.html")

    def test_recipe_create_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class RecipeUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.flour = Ingredient.objects.create(
            user=self.user,
            name="Flour",
        )
        self.chocolate_bar = Ingredient.objects.create(
            user=self.user,
            name="Chocolate Bar",
        )
        self.recipe = Recipe.objects.create(user=self.user, name="Chocolate Cake")
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.flour,
            qty_needed=Decimal("100"),
        )
        self.url = reverse("production:recipe_edit", kwargs={"pk": self.recipe.pk})

    def test_recipe_update_view_renders_object_and_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/form.html")

    def test_recipe_update_view_renders_success_template(self):
        response = self.client.post(
            self.url,
            data={
                "name": "Updated name",
                "description": "Lorem Ipsum",
                "ingredient_ids": [self.flour.id],
                "quantities": Decimal("100"),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/oob/_update_success.html")

    def test_recipe_update_view_renders_form_error_when_blank_name(self):
        response = self.client.post(
            self.url,
            data={
                "name": " ",
                "description": "Lorem Ipsum",
                "ingredient_ids": [self.flour.id],
                "quantities": Decimal("100"),
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "production/recipe/oob/_form_error.html")

    def test_recipe_update_view_renders_error_toast_when_zero_ingredient(
        self,
    ):
        response = self.client.post(
            self.url,
            data={
                "name": "Chocolate Cake",
                "description": "Lorem Ipsum",
                "ingredient_ids": [],
                "quantities": Decimal("100"),
            },
        )
        self.assertTemplateUsed(response, "components/toast/_toast_oob.html")

    def test_recipe_update_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )
