from django.contrib import admin

from .models import (RecipeIngredient, PurchaseItem,
                     Favorite, Follow, Ingredient, Recipe)


class MemdershipInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    def recipe_favorite_count(self, obj):
        return obj.favorites.count()
    recipe_favorite_count.short_description = "В избранном"

    list_display = ("title", "pub_date", "author",
                    "time_cooking", 'recipe_favorite_count')
    search_fields = ("title", "text",)
    list_filter = ("tag_breakfast", "tag_lunch",
                   "tag_dinner", "pub_date", "author",)
    inlines = [MemdershipInline]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension",)
    search_fields = ("title", )
    list_filter = ("dimension", )


admin.site.register(PurchaseItem)
admin.site.register(Favorite)
admin.site.register(Follow)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
