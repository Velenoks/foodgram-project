from django.shortcuts import render

from recipes.models import Recipe


def index(request):
    recipes = Recipe.objects.all()
    return render(
        request,
        "index.html",
        {
            "recipes": recipes,
        },
    )
