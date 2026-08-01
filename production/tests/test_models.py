from decimal import Decimal
from datetime import date, timedelta
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from inventory.models import Ingredient, IngredientPurchase
from ..models import Recipe, RecipeIngredient, ProductionBatch


class RecipeModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.flour = Ingredient.objects.create(
            user=self.user,
            name="Flour",
            unit="g",
        )
        self.chocolate_bar = Ingredient.objects.create(
            user=self.user,
            name="Chocolate Bar",
            unit="g",
        )

        self.recipe = Recipe.objects.create(user=self.user, name="Cake")

        RecipeIngredient.objects.bulk_create(
            [
                RecipeIngredient(
                    recipe=self.recipe,
                    ingredient=self.flour,
                    qty_needed=Decimal("50"),
                ),
                RecipeIngredient(
                    recipe=self.recipe,
                    ingredient=self.chocolate_bar,
                    qty_needed=Decimal("50"),
                ),
            ]
        )

    def test_string_representation_returns_name(self):
        self.assertEqual(str(self.flour), "Flour")

    def test_get_absolute_url_returns_correct_url(self):
        self.assertEqual(
            self.recipe.get_absolute_url(),
            reverse("production:recipe", kwargs={"pk": self.recipe.pk}),
        )

    def test_get_all_ingredients_returns_all_recipe_ingredients(self):
        ingredient_requirements = self.recipe.get_all_ingredients()
        self.assertEqual(len(ingredient_requirements), 2)
        self.assertEqual(ingredient_requirements[0].ingredient, self.flour)

    def test_get_ingredient_ids_returns_ingredient_ids(self):
        ingredient_ids = list(self.recipe.get_ingredient_ids())
        self.assertEqual(
            ingredient_ids,
            [self.flour.id, self.chocolate_bar.id],
        )

    def test_total_cost_returns_correct_calculation(self):
        IngredientPurchase.objects.create(
            ingredient=self.flour,
            qty_purchased=Decimal("100"),
            purchased_at=date.today(),
            total_cost=Decimal("300"),
        )
        expected = sum(
            ingredient.ingredient_cost
            for ingredient in self.recipe.get_all_ingredients()
        )
        self.assertEqual(
            self.recipe.total_cost,
            expected,
        )

    def test_is_recently_added_returns_correct_time_diff(self):
        self.recipe.created_at = timezone.now() - timedelta(days=10)
        self.recipe.save(update_fields=["created_at"])
        self.assertTrue(self.recipe.is_recently_added)

    def test_is_recently_added_returns_false_when_created_more_than_15_days_ago(self):
        self.recipe.created_at = timezone.now() - timedelta(days=16)
        self.recipe.save(update_fields=["created_at"])
        self.assertFalse(self.recipe.is_recently_added)


class RecipeIngredientModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.flour = Ingredient.objects.create(
            user=self.user,
            name="Flour",
            unit="g",
        )
        self.recipe = Recipe.objects.create(user=self.user, name="Cake")
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.flour,
            qty_needed=Decimal("50"),
        )

    def test_recipe_ingredient_cost_returns_correct_calculation(self):
        IngredientPurchase.objects.create(
            ingredient=self.flour,
            qty_purchased=Decimal("100"),
            purchased_at=date.today(),
            total_cost=Decimal("300"),
        )
        self.assertEqual(self.recipe_ingredient.ingredient_cost, Decimal("150"))


class ProductionBatchModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="Mike", password="testpass123"
        )
        self.flour = Ingredient.objects.create(
            user=self.user,
            name="Flour",
            unit="g",
        )
        self.recipe = Recipe.objects.create(user=self.user, name="Cake")
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.flour,
            qty_needed=Decimal("50"),
        )
        self.production_batch = ProductionBatch.objects.create(
            user=self.user,
            recipe=self.recipe,
            recipe_name="Recipe",
            est_cost=Decimal("100"),
            batch_qty=Decimal("1"),
        )

    def test_get_absolute_url_returns_correct_url(self):
        self.assertEqual(
            self.production_batch.get_absolute_url(),
            reverse("production:batch", kwargs={"pk": self.production_batch.pk}),
        )

    def test_production_batch_returns_pending_status(self):
        self.assertEqual(
            self.production_batch.status, self.production_batch.Status.PENDING
        )

    def test_production_batch_returns_IN_PROGRESS_status(self):
        self.production_batch.status = "I"
        self.assertEqual(
            self.production_batch.status, self.production_batch.Status.IN_PROGRESS
        )

    def test_production_batch_returns_COMPLETE_status(self):
        self.production_batch.status = "C"
        self.assertEqual(
            self.production_batch.status, self.production_batch.Status.COMPLETE
        )

    def test_production_batch_returns_CANCELLED_status(self):
        self.production_batch.status = "X"
        self.assertEqual(
            self.production_batch.status, self.production_batch.Status.CANCELLED
        )


class BatchIngredientModelTests(TestCase):
    pass
