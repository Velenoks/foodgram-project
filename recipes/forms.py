from django import forms

from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'tag_breakfast',
            'tag_lunch', 'tag_dinner', 'ingredient',
            'time_cooking', 'text', 'image'
        ]


class IngredientRecipeForm(forms.ModelForm):
    recipe = RecipeForm()

    class Meta:
        model = RecipeIngredient
        fields = (
            'ingredient', 'count', 'recipe'
        )
