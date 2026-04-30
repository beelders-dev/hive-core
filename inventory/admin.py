from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient

# Register your models here.


# class RecipeRequirementInline(admin.TabularInline):
#     model = RecipeRequirement
#     fk_name = "parent_recipe"
#     extra = 1


class IngredientAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "stock_qty",
        "price",
    ]


class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    # inlines = [RecipeRequirementInline]


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = [
        "recipe",
        "ingredient",
        "quantity_needed",
    ]


# class ReceipeRequirementAdmin(admin.ModelAdmin):
#     list_display = [
#         "parent_recipe",
#         "child_recipe",
#     ]


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
# admin.site.register(RecipeRequirement, ReceipeRequirementAdmin)
