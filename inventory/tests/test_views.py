from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
from ..models import Ingredient, IngredientPurchase, PurchaseAdjustment


class InventoryHomeViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("inventory:index")

    def test_inventory_home_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "inventory/index.html")

    def test_inventory_home_view_displays_page_header(self):
        response = self.client.get(self.url)
        self.assertContains(response, "Ingredients")

    def test_inventory_home_view_has_results_ingredient_list_context(self):
        response = self.client.get(self.url)
        self.assertQuerySetEqual(
            response.context["ingredient_list"],
            Ingredient.objects.filter(user=self.user),
        )

    def test_inventory_home_view_has_results_url_context(self):
        response = self.client.get(self.url)
        self.assertIn("results_url", response.context)

    def test_inventory_home_view_is_inaccessible_when_logged_out(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)


class IngredientListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("inventory:ingredient_list")

    def test_ingredient_list_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(
            response, "inventory/ingredient/partials/_results_table.html"
        )

    def test_ingredient_list_view_renders_ingredient(self):
        Ingredient.objects.create(user=self.user, name="Flour")
        response = self.client.get(self.url)
        self.assertContains(response, "Flour")

    def test_test_ingredient_list_view_search_returns_matching_ingredients(self):
        Ingredient.objects.create(user=self.user, name="Sugar")
        Ingredient.objects.create(user=self.user, name="Flour")
        response = self.client.get(self.url, {"q": "sug"})
        self.assertContains(response, "Sugar")
        self.assertNotContains(response, "Flour")

    def test_test_ingredient_list_view_search_strips_whitespace(self):
        Ingredient.objects.create(user=self.user, name="Sugar")
        response = self.client.get(self.url, {"q": "  Sugar   "})
        self.assertContains(response, "Sugar")

    def test_empty_search_returns_all_ingredients(self):
        Ingredient.objects.create(user=self.user, name="Sugar")
        Ingredient.objects.create(user=self.user, name="Flour")
        response = self.client.get(self.url, {"q": ""})
        self.assertContains(response, "Sugar")
        self.assertContains(response, "Flour")

    def test_missing_search_parameter_returns_all_ingredients(self):
        Ingredient.objects.create(user=self.user, name="Sugar")
        response = self.client.get(self.url)
        self.assertContains(response, "Sugar")

    def test_ingredient_list_view_not_viewable_when_user_is_logged_out(self):
        self.client.logout()
        response = self.client.get(self.url, {"q": "sugar"})
        self.assertEqual(response.status_code, 302)

    def test_ingredient_list_view_not_viewable_when_different_user_is_logged_in(self):
        Ingredient.objects.create(user=self.user, name="Flour")
        self.client.logout()
        another_user = get_user_model().objects.create_user(
            username="Wela", password="testpass123"
        )
        self.client.force_login(another_user)
        another_user_ingredient = Ingredient.objects.create(
            user=another_user, name="Sugar"
        )
        response = self.client.get(reverse("inventory:ingredient_list"))
        ingredients = response.context["ingredient_list"]
        self.assertEqual(list(ingredients), [another_user_ingredient])


class IngredientCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("inventory:ingredient_create")

    def test_ingredient_create_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/ingredient/form.html")

    def test_ingredient_create_view_renders_success_template(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "Cocoa Powder",
                "unit": "g",
                "low_stock_threshold": "100",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "inventory/ingredient/oob/_create_success.html"
        )

    def test_ingredient_create_view_renders_ingredient_created(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "Cocoa Powder",
                "unit": "g",
                "low_stock_threshold": "100",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cocoa Powder")


class IngredientUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.url = reverse(
            "inventory:ingredient_update", kwargs={"pk": self.ingredient.pk}
        )

    def test_ingredient_update_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/ingredient/form.html")

    def test_ingredient_update_view_renders_success_template(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "Cocoa Powder",
                "unit": "g",
                "low_stock_threshold": "200",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "inventory/ingredient/oob/_create_success.html"
        )
