from django.core.exceptions import ValidationError
from decimal import Decimal
from django.test import TestCase
from django.urls import reverse

from .models import Ingredient

# Create your tests here.


class IngredientModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.ingredient = Ingredient.objects.create(
            name="egg", stock_qty=12.00, price=25.00
        )

    def test_ingredient_content(self):
        self.assertEqual(self.ingredient.name, "egg")
        self.assertEqual(self.ingredient.stock_qty, Decimal(12.00))
        self.assertEqual(self.ingredient.price, Decimal(25.00))

    def test_ingredient_str(self):
        expected = "egg  (12.00g)"
        self.assertEqual(str(self.ingredient), expected)

    def test_get_absolute_url_returns_correct_url(self):
        self.assertEqual(
            self.ingredient.get_absolute_url(),
            reverse("inventory:ingredient", kwargs={"pk": self.ingredient.pk}),
        )

    def test_get_total_amount_calculates_correctly(self):
        self.assertEqual(self.ingredient.get_total_amount(), Decimal(300.00))

    def test_stock_cannot_be_negative(self):
        invalid_ingredient = Ingredient.objects.create(
            name="apple", stock_qty=-20.00, price=25.00
        )
        with self.assertRaises(ValidationError):
            invalid_ingredient.full_clean()

    def test_price_cannot_be_negative(self):
        invalid_ingredient = Ingredient.objects.create(
            name="apple", stock_qty=20.00, price=-25.00
        )
        with self.assertRaises(ValidationError):
            invalid_ingredient.full_clean()


class IngredientListViewTests(TestCase):

    def setUp(self):
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


class IngredientCreateViewTests(TestCase):

    def setUp(self):
        self.url = reverse("inventory:ingredient_add")

    def test_create_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_create_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "inventory/ingredient_form.html")

    def test_create_view_valid_post_creates_ingredient(self):
        self.client.post(
            self.url,
            {
                "name": "Butter",
                "stock_qty": 20,
                "unit": "g",
                "price": 15,
            },
        )
        self.assertEqual(Ingredient.objects.count(), 1)

    def test_create_view_invalid_post_does_not_create_ingredient(self):
        response = self.client.post(
            self.url,
            {
                "name": "",
                "stock_qty": 20,
                "unit": "g",
                "price": 15,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_create_view_successful_post_redirects(self):
        response = self.client.post(
            self.url,
            {
                "name": "Butter",
                "stock_qty": 20,
                "unit": "g",
                "price": 12,
            },
        )

        self.assertRedirects(response, reverse("inventory:ingredient_list"))


class IngredientUpdateViewTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Egg", stock_qty=10, price=20)
        self.url = reverse(
            "inventory:ingredient_update", kwargs={"pk": self.ingredient.pk}
        )

    def test_update_view_displays_correctly(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/ingredient_form.html")

    def test_update_view_valid_post_updates_ingredient(self):
        response = self.client.post(
            self.url,
            data={
                "name": "Egg",
                "unit": "g",
                "stock_qty": 20,
                "price": 20,
            },
        )
        self.ingredient.refresh_from_db()
        self.assertRedirects(response, reverse("inventory:ingredient_list"))
        self.assertEqual(self.ingredient.stock_qty, 20)

    def test_update_view_invalid_post_does_not_update_ingredient(self):
        original_name = self.ingredient.name
        response = self.client.post(
            self.url,
            data={
                "name": "",
                "unit": "g",
                "stock_qty": 10,
                "price": 20,
            },
        )
        self.ingredient.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.ingredient.name, original_name)

    def test_update_view_successful_post_redirects(self):
        response = self.client.post(
            self.url,
            data={
                "name": "Butter",
                "unit": "g",
                "stock_qty": 20,
                "price": 12,
            },
        )

        self.assertRedirects(response, reverse("inventory:ingredient_list"))


class IngredientDeleteViewTests(TestCase):

    def setUp(self):
        self.ingredient = Ingredient.objects.create(name="Egg", stock_qty=10, price=20)
        self.url = reverse(
            "inventory:ingredient_delete", kwargs={"pk": self.ingredient.pk}
        )

    def test_delete_view_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_delete_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "inventory/ingredient_delete.html")

    def test_delete_view_deletes_ingredient(self):
        self.client.post(self.url)
        self.assertEqual(Ingredient.objects.count(), 0)

    def test_delete_view_redirects_after_successful_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse("inventory:ingredient_list"))
