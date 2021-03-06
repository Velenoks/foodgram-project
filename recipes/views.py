import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RecipeForm
from .models import (Recipe, Follow, USER,
                     Favorite, RecipeIngredient, PurchaseItem)
from .helpers import parser_ingredients, ingredients_in_text, tag_filter


def index(request):
    recipes = Recipe.objects.all().select_related(
        'author',
    )
    if request.user.is_authenticated:
        recipes = recipes.annotate(
            is_favorite=Exists(
                Favorite.objects.filter(
                    user=request.user, recipe_id=OuterRef('pk')
                )
            )
        ).annotate(
            is_purchase=Exists(
                PurchaseItem.objects.filter(
                    user=request.user, recipe_id=OuterRef('pk')
                )
            )
        )
    recipes = tag_filter(request, recipes)
    paginator = Paginator(recipes, settings.ELEMENTS_ON_PAGE)
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
    follow = False
    recipes = Recipe.objects.filter(author=author).select_related(
        'author',
    )
    if request.user.is_authenticated:
        follow = Follow.objects.filter(
            user=request.user, author=author
        ).exists()
        recipes = recipes.annotate(
            is_favorite=Exists(
                Favorite.objects.filter(
                    user=request.user, recipe_id=OuterRef('pk')
                )
            )
        ).annotate(
            is_purchase=Exists(
                PurchaseItem.objects.filter(
                    user=request.user, recipe_id=OuterRef('pk')
                )
            )
        )
    recipes = tag_filter(request, recipes)
    paginator = Paginator(recipes, settings.ELEMENTS_ON_PAGE)
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
    recipes = Recipe.objects.all().select_related(
        'author',
    ).annotate(
        is_favorite=Exists(
            Favorite.objects.filter(
                user=request.user, recipe_id=OuterRef('pk')
            )
        )
    ).filter(is_favorite=True).annotate(
        is_purchase=Exists(
            PurchaseItem.objects.filter(
                user=request.user, recipe_id=OuterRef('pk')
            )
        )
    )
    recipes = tag_filter(request, recipes)
    paginator = Paginator(recipes, settings.ELEMENTS_ON_PAGE)
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
    users = USER.objects.filter(
        following__user=request.user
    ).annotate(
        recipes_count=Count('recipes')
    ).prefetch_related(
        'recipes',
    ).order_by('username')
    paginator = Paginator(users, settings.ELEMENTS_ON_PAGE)
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
    title = "???????????????? ??????????????"
    save_button = "?????????????? ????????????"
    if request.POST:
        ingredients = parser_ingredients(request.POST)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None)
    if form.is_valid():
        create_recipe = form.save(commit=False)
        create_recipe.author = request.user
        create_recipe.save()
        recipe = Recipe.objects.latest('pk')
        for ingredient in ingredients:
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient[0],
                                            count=ingredient[1])
        return redirect("index")
    return render(
        request,
        "new_and_edit_recipe.html",
        {
            "form": form,
            "title": title,
            "save_button": save_button
        },
    )


@login_required()
def edit_recipe(request, recipe_id):
    title = "???????????????????????????? ??????????????"
    save_button = "??????????????????"
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    if request.POST:
        ingredients = parser_ingredients(request.POST)
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if form.is_valid():
        form.save()
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients:
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient[0],
                                            count=ingredient[1])
        return redirect("recipe", recipe_id=recipe_id)
    return render(
        request,
        "new_and_edit_recipe.html",
        {
            "recipe": recipe,
            "form": form,
            "title": title,
            "save_button": save_button
        },
    )


@login_required()
def delete_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id, author=request.user)
    recipe.delete()
    return redirect("user_recipe", username=request.user.username)


def recipe_view(request, recipe_id):
    recipe = Recipe.objects.filter(pk=recipe_id)
    follow = False
    if request.user.is_authenticated:
        recipe = recipe.annotate(
            is_favorite=Exists(
                Favorite.objects.filter(
                    user_id=request.user.pk, recipe_id=recipe_id
                )
            )
        ).annotate(
            is_purchase=Exists(
                PurchaseItem.objects.filter(
                    user=request.user, recipe_id=OuterRef('pk')
                )
            )
        )
        follow = Follow.objects.filter(user=request.user,
                                       author=recipe[0].author).exists()
    return render(
        request,
        "recipe.html",
        {"recipe": recipe[0], "follow": follow}
    )


@login_required()
def purchase_view(request):
    recipes = Recipe.objects.all().annotate(is_purchase=Exists(
        PurchaseItem.objects.filter(
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    )).filter(is_purchase=True)
    return render(
        request,
        "purchases_list.html",
        {"recipes": recipes}
    )


@login_required()
def download_purchases(request):
    purchases = PurchaseItem.objects.filter(user=request.user)
    recipes = Recipe.objects.filter(purchase__in=purchases)
    full_name = request.user.get_full_name()
    items = RecipeIngredient.objects.filter(recipe__in=recipes)
    content = f"?????????? {datetime.datetime.now()}\n" \
              f"?????????? ???????????????? - {recipes.count()}\n" \
              f"???????????? ?????????????????? ?????? {full_name}\n" \
              "??????????????????????:\n" + ingredients_in_text(items)
    filename = f"purchase_{request.user.username}.txt"
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename={0}".format(
        filename)
    return response


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(
        request,
        "misc/500.html",
        status=500
    )
