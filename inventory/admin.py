from django.contrib import admin

from .models import Ingredient

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


admin.site.register(Ingredient, IngredientAdmin)
