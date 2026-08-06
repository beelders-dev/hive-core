from datetime import date
from decimal import Decimal
from django.utils import timezone
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from inventory.models import Ingredient, IngredientPurchase
from production.models import Recipe, RecipeIngredient, ProductionBatch


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


class AddIngredientViewTests(TestCase):
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
        self.url = reverse(
            "production:add_ingredient",
            kwargs={
                "pk": self.chocolate_bar.pk,
            },
        )

    def test_add_ingredient_view_adds_and_posts_ingredient_successfully(self):
        response = self.client.post(
            self.url,
            data={
                "ingredient_ids": [str(self.flour.pk)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chocolate Bar")
        self.assertNotContains(response, "Flour")

    def test_add_ingredient_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class RemoveIngredientViewTests(TestCase):
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
        self.url = reverse(
            "production:remove_ingredient",
            kwargs={
                "pk": self.chocolate_bar.pk,
            },
        )

    def test_remove_ingredient_view_removes_and_posts_ingredient_successfully(self):
        response = self.client.post(
            self.url,
            data={
                "ingredient_ids": [str(self.chocolate_bar.pk)],
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Flour")
        self.assertNotContains(response, "Chocolate bar")

    def test_remove_ingredient_view_requires_login(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={self.url}",
        )


class CreateBatchViewTests(TestCase):
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
        IngredientPurchase.objects.create(
            ingredient=self.flour,
            purchased_at=date.today(),
            qty_purchased=Decimal("300"),
            total_cost=Decimal("300"),
        )

        self.recipe = Recipe.objects.create(user=self.user, name="Chocolate Cake")

        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.flour,
            qty_needed=Decimal("100"),
        )
        self.url = reverse(
            "production:create_batch",
            kwargs={
                "pk": self.recipe.pk,
            },
        )

    def test_create_batch_view_is_executed_when_recipe_is_created(self):
        response = self.client.post(
            self.url,
            data={"recipe": self.recipe.pk},
            HTTP_HX_REQUEST="true",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductionBatch.objects.count(), 1)
        batch = ProductionBatch.objects.get()
        self.assertEqual(batch.recipe, self.recipe)
        self.assertTemplateUsed(response, "production/batch/oob/_create_success.html")


class ProductionDashboardViewTests(TestCase):

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
        IngredientPurchase.objects.create(
            ingredient=self.flour,
            purchased_at=date.today(),
            qty_purchased=Decimal("300"),
            total_cost=Decimal("300"),
        )

        self.recipe = Recipe.objects.create(user=self.user, name="Chocolate Cake")

        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.flour,
            qty_needed=Decimal("100"),
        )
        self.batch = ProductionBatch.objects.create(
            user=self.user,
            recipe=self.recipe,
            batch_qty=Decimal("100"),
            recipe_name=self.recipe.name,
            est_cost=Decimal("100"),
        )
        self.url = reverse(
            "production:index",
        )

    def test_production_dashboard_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "production/index.html")

    def test_production_dashboard_renders_recipe(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["recipes"][0], self.recipe)

    def test_production_dashboard_renders_batch(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context["batches"][0], self.batch)

    def test_production_dashboard_renders_completed_today(self):
        self.batch.completed_at = timezone.now()
        self.batch.save()
        response = self.client.get(self.url)
        self.assertEqual(response.context["completed_today"], 1)


class BatchDetailViewTests(TestCase):

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
        IngredientPurchase.objects.create(
            ingredient=self.flour,
            purchased_at=date.today(),
            qty_purchased=Decimal("300"),
            total_cost=Decimal("300"),
        )

        self.recipe = Recipe.objects.create(user=self.user, name="Chocolate Cake")

        RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.flour,
            qty_needed=Decimal("100"),
        )
        self.batch = ProductionBatch.objects.create(
            user=self.user,
            recipe=self.recipe,
            batch_qty=Decimal("100"),
            recipe_name=self.recipe.name,
            est_cost=Decimal("100"),
        )
        self.url = reverse(
            "production:batch",
            kwargs={
                "pk": self.batch.pk,
            },
        )

    def test_batch_detail_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "production/batch/detail.html")
