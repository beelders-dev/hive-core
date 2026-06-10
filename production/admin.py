from django.contrib import admin

from .models import Recipe, RecipeIngredient


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
        "quantity_needed",
    ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
