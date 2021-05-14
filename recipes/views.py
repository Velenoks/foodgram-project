from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from recipes.forms import RecipeForm
from recipes.models import Recipe, Follow


def index(request):
    recipes = Recipe.objects.all()
    return render(
        request,
        "index.html",
        {
            "recipes": recipes,
        },
    )

@login_required()
def new_recipe(request):
    title = "Создание рецепта"
    save_button = "Создать репепт"
    form = RecipeForm(request.POST or None,
                    files=request.FILES or None)
    if form.is_valid():
        create_recipe = form.save(commit=False)
        create_recipe.user = request.user
        create_recipe.save()
        return redirect("index")
    return render(
        request,
        "new_recipe.html",
        {
            "form": form,
            "title": title,
            "save_button": save_button
        },
    )

def recipe_view(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = recipe.user
    following = False
    if request.user.is_authenticated:
        if Follow.objects.filter(user=request.user, author=user).exists():
            following = True
    return render(
        request,
        "recipe.html",
        {"recipe": recipe, "user": user, "following": following }
    )
