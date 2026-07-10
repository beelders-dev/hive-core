from django.contrib import admin

from .models import Recipe, RecipeIngredient, BatchIngredient, ProductionBatch


# Register your models here.
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    # inlines = [RecipeRequirementInline]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = [
        "recipe",
        "ingredient",
        "qty_needed",
    ]


@admin.register(ProductionBatch)
class ProductionBatchAdmin(admin.ModelAdmin):
    list_display = [
        "recipe",
        "batch_qty",
        "notes",
        "recipe_name",
        "est_cost",
    ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
