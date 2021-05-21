from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Count
from django.shortcuts import render, redirect, get_object_or_404

from recipes.forms import RecipeForm
from recipes.models import Recipe, Follow, USER, Favorite


def index(request):
    recipes = Recipe.objects.all().annotate(is_favorite=Exists(
            Favorite.objects.filter(
                user_id=request.user.pk,
                recipe_id=OuterRef('pk'),
            ),
        ))
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {
            "page": page,
            "paginator": paginator,
        },
    )


def user_recipe(request, username):
    author = get_object_or_404(USER, username=username)
    follow = Follow.objects.filter(user=request.user, author=author).exists()
    recipes = Recipe.objects.filter(author=author).annotate(is_favorite=Exists(
            Favorite.objects.filter(
                user_id=request.user.pk,
                recipe_id=OuterRef('pk'),
            ),
        ))
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "user_recipe.html",
        {
            "page": page,
            "paginator": paginator,
            "author": author,
            "follow": follow
        },
    )


@login_required()
def favorite(request):
    recipes = Recipe.objects.all().annotate(is_favorite=Exists(
            Favorite.objects.filter(
                user_id=request.user.pk,
                recipe_id=OuterRef('pk'),
            ),
        )).filter(is_favorite=True)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "favorite.html",
        {
            "page": page,
            "paginator": paginator,
        },
    )


@login_required()
def follow(request):
    users = USER.objects.filter(following__user=request.user).annotate(recipes_count=Count('recipes'))
    paginator = Paginator(users, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(
        request,
        "follow.html",
        {
            "page": page,
            "paginator": paginator,
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
    recipe = Recipe.objects.filter(pk=recipe_id).annotate(is_favorite=Exists(
            Favorite.objects.filter(
                user_id=request.user.pk,
                recipe_id=recipe_id,
            ),
        ))[0]
    follow = Follow.objects.filter(user=request.user, author=recipe.author).exists()
    print(follow)
    return render(
        request,
        "recipe.html",
        {"recipe": recipe, "follow": follow}
    )
