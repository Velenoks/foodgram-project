from django.contrib import admin
from .models import *


class MemdershipInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    inlines = [MemdershipInline]

admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
