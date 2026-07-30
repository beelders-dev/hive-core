from datetime import date
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

    def test_inventory_home_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class IngredientListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("inventory:list")

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

    def test_ingredient_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )

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
        response = self.client.get(reverse("inventory:list"))
        ingredients = response.context["ingredient_list"]
        self.assertEqual(list(ingredients), [another_user_ingredient])


class IngredientCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.url = reverse("inventory:create")

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

    def test_ingredient_create_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class IngredientUpdateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.url = reverse("inventory:update", kwargs={"pk": self.ingredient.pk})

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
            response, "inventory/ingredient/oob/_update_success.html"
        )

    def test_ingredient_update_view_ingredient_updated(self):
        response = self.client.post(
            self.url,
            data={
                "user": self.user,
                "name": "Cocoa Powder Updated",
                "unit": "g",
                "low_stock_threshold": "200",
            },
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cocoa Powder Updated")

    def test_ingredient_update_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class IngredientDeleteViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.url = reverse("inventory:delete", kwargs={"pk": self.ingredient.pk})

    def test_ingredient_delete_view_renders_object_and_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.ingredient)
        self.assertTemplateUsed(response, "inventory/ingredient/delete.html")

    def test_ingredient_delete_view_redirects_to_inventory_home_after_delete(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("inventory:index"))

    def test_ingredient_delete_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class IngredientDetailViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.url = reverse("inventory:ingredient", kwargs={"pk": self.ingredient.pk})

    def test_ingredient_detail_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/ingredient/detail.html")

    def test_ingredient_detail_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class PurchaseListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.purchase = IngredientPurchase.objects.create(
            ingredient=self.ingredient,
            purchased_at=timezone.now(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )
        self.url = reverse("inventory:purchase_list", kwargs={"pk": self.ingredient.pk})

    def test_purchase_list_view_renders_object_and_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        purchases = response.context["purchases"]
        self.assertEqual(list(purchases), [self.purchase])
        self.assertTemplateUsed(response, "inventory/purchase/partials/_list.html")

    def test_purchase_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class PurchaseDetailViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.purchase = IngredientPurchase.objects.create(
            ingredient=self.ingredient,
            purchased_at=timezone.now(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )
        self.url = reverse("inventory:purchase", kwargs={"pk": self.purchase.pk})

    def test_purchase_detail_view_renders_object_and_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        purchase = response.context["purchase"]
        self.assertEqual(purchase, self.purchase)
        self.assertTemplateUsed(response, "inventory/purchase/detail.html")

    def test_purchase_detail_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class PurchaseCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.url = reverse(
            "inventory:purchase_create", kwargs={"pk": self.ingredient.pk}
        )

    def test_purchase_create_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/purchase/form.html")

    def test_purchase_create_view_renders_success_template_after_create(self):
        response = self.client.post(
            self.url,
            data={
                "purchased_at": date.today(),
                "qty_purchased": Decimal("100"),
                "total_cost": Decimal("100"),
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/purchase/oob/_create_success.html")

    def test_purchase_create_view_creates_purchase_successfully(self):
        self.client.post(
            self.url,
            data={
                "purchased_at": date.today(),
                "qty_purchased": Decimal("100"),
                "total_cost": Decimal("100"),
            },
            HTTP_HX_REQUEST="true",
        )
        purchase = IngredientPurchase.objects.get()
        self.assertEqual(purchase.ingredient, self.ingredient)

    def test_purchase_create_view_does_not_create_with_zero_total_cost(self):
        self.client.post(
            self.url,
            data={
                "purchased_at": date.today(),
                "qty_purchased": Decimal("100"),
                "total_cost": "",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(IngredientPurchase.objects.count(), 0)

    def test_purchase_create_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class PurchaseUpdateViewTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.purchase = IngredientPurchase.objects.create(
            ingredient=self.ingredient,
            purchased_at=date.today(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )
        self.url = reverse("inventory:purchase_update", kwargs={"pk": self.purchase.pk})

    def test_purchase_update_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/purchase/form.html")

    def test_purchase_update_view_renders_success_template(self):
        response = self.client.post(
            self.url,
            data={
                "purchased_at": date.today(),
                "qty_purchased": Decimal("100"),
                "total_cost": Decimal("100"),
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/purchase/oob/_edit_success.html")

    def test_purchase_update_view_does_not_update_purchase_when_form_is_invalid(self):
        response = self.client.post(
            self.url,
            data={
                "purchased_at": date.today(),
                "qty_purchased": Decimal("100"),
                "total_cost": "",
            },
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 400)

        self.assertTemplateUsed(response, "inventory/purchase/form.html")
        self.purchase.refresh_from_db()
        self.assertEqual(self.purchase.total_cost, Decimal("100"))

    def test_purchase_update_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class PurchaseAdjustmentListView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.purchase = IngredientPurchase.objects.create(
            ingredient=self.ingredient,
            purchased_at=date.today(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )
        self.adjustment = PurchaseAdjustment.objects.create(
            purchase=self.purchase,
            qty_adjustment=Decimal("100"),
        )

        self.url = reverse("inventory:adjustment_list", kwargs={"pk": self.purchase.pk})

    def test_purchase_adjustment_list_view_renders_objects_and_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        adjustments = response.context["adjustment_list"]
        self.assertEqual(list(adjustments), [self.adjustment])
        self.assertTemplateUsed(response, "inventory/adjustment/partials/_list.html")

    def test_purchase_adjustment_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class PurchaseAdjustmentCreateView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.client.force_login(self.user)
        self.ingredient = Ingredient.objects.create(user=self.user, name="Cocoa Powder")
        self.purchase = IngredientPurchase.objects.create(
            ingredient=self.ingredient,
            purchased_at=date.today(),
            qty_purchased=Decimal("100"),
            total_cost=Decimal("100"),
        )

        self.url = reverse(
            "inventory:adjustment_create",
            kwargs={"pk": self.purchase.pk},
        )

    def test_purchase_adjustment_create_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "inventory/adjustment/partials/_form.html")

    def test_purchase_adjustment_create_view_renders_success_template(self):
        response = self.client.post(
            self.url,
            data={
                "qty_adjustment": Decimal("-50"),
                "note": "Adjustment",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "inventory/adjustment/oob/_create_success.html"
        )

    def test_purchase_adjustment_create_view_does_not_save_when_qty_is_negative(self):
        response = self.client.post(
            self.url,
            data={
                "qty_adjustment": Decimal("-150"),
                "note": "Adjustment",
            },
        )
        self.purchase.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.purchase.total_stocks_plus_adjustments, Decimal("100"))
        self.assertEqual(self.purchase.adjustments.count(), 0)
        self.assertContains(response, "Adjustment cannot reduce stock below zero.")

    def test_purchase_adjustment_create_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )
