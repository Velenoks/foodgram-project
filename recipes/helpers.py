from django.shortcuts import get_object_or_404

from .models import Ingredient


def parser_ingredients(data):
    ingredients = []
    keys_ingredients = []
    keys = data.keys()
    for key in keys:
        if 'nameIngredient' in key or 'valueIngredient' in key:
            keys_ingredients.append(key)
    lens = len(keys_ingredients)
    for i in range(0, lens, 2):
        ingredient = get_object_or_404(Ingredient,
                                       title=data[keys_ingredients[i]])
        count = int(data[keys_ingredients[i + 1]])
        ingredients.append((ingredient, count))
    return ingredients


def ingredients_in_text(items):
    ingredients = {}
    for itm in items:
        try:  # Прибавить к имеющемуся
            ingredients[itm.ingredient.title]["value"] += itm.count
        except KeyError:  # Добавить новый ингредиент
            ingredients[itm.ingredient.title] = {
                "value": itm.count,
                "dimension": itm.ingredient.dimension
            }
    text = ''
    for ingredient in ingredients:
        text += f"{ingredient} - {ingredients[ingredient]['value']} " \
                f"{ingredients[ingredient]['dimension']}\n"
    return text


def tag_filter(request, recipes):
    tags = request.GET.getlist('tag')
    if 'tag_breakfast' in tags:
        recipes = recipes.filter(tag_breakfast=True)
    if 'tag_lunch' in tags:
        recipes = recipes.filter(tag_lunch=True)
    if 'tag_dinner' in tags:
        recipes = recipes.filter(tag_dinner=True)
    return recipes
