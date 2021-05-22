from django.shortcuts import get_object_or_404

from recipes.models import Ingredient


def parser_ingredients(data):
    ingredients = []
    keys_ingredients = []
    keys = data.keys()
    for key in keys:
        if 'nameIngredient' in key or 'valueIngredient' in key:
            keys_ingredients.append(key)
    lens = len(keys_ingredients)
    for i in range(0, lens, 2):
        ingredient = get_object_or_404(Ingredient, title=data[keys_ingredients[i]])
        count = int(data[keys_ingredients[i+1]])
        ingredients.append((ingredient, count))
    return ingredients