from django.contrib import admin
from .models import Ingredient, IngredientPurchase, PurchaseAdjustment


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "unit",
        "low_stock_threshold",
    ]


@admin.register(IngredientPurchase)
class IngredientPurchaseAdmin(admin.ModelAdmin):
    list_display = [
        "purchased_at",
        "exp_date",
        "qty_purchased",
        "total_cost",
    ]


@admin.register(PurchaseAdjustment)
class PurchaseAdjustmentAdmin(admin.ModelAdmin):
    list_display = ["qty_adjustment"]
