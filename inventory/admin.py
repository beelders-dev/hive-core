from django.contrib import admin

from .models import Ingredient, IngredientPurchase


class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "unit",
        "low_stock_threshold",
    ]


class IngredientPurchaseAdmin(admin.ModelAdmin):
    list_display = [
        "purchased_at",
        "exp_date",
        "qty_purchased",
        "total_cost",
    ]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientPurchase, IngredientPurchaseAdmin)
