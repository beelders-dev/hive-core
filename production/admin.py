from django.contrib import admin

from .models import Recipe, RecipeIngredient, RecipeDraft, RecipeDraftIngredient


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


class RecipeDraftAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


class RecipeDraftIngredientAdmin(admin.ModelAdmin):
    list_display = [
        "ingredient",
        "required_quantity",
    ]


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(RecipeDraft, RecipeDraftAdmin)
admin.site.register(RecipeDraftIngredient, RecipeDraftIngredientAdmin)
