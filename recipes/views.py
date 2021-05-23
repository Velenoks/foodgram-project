import datetime
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Exists, OuterRef, Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from recipes.forms import RecipeForm
from recipes.models import Recipe, Follow, USER, Favorite, RecipeIngredient, PurchaseItem
from recipes.helpers import parser_ingredients, ingredients_in_text


def index(request):
    recipes = Recipe.objects.all().annotate(is_favorite=Exists(
        Favorite.objects.filter(
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    )).annotate(is_purchase=Exists(
        PurchaseItem.objects.filter(
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    ))
    tags = request.GET.getlist('tag')
    if 'tag_breakfast' in tags:
        recipes = recipes.filter(tag_breakfast=True)
    if 'tag_lunch' in tags:
        recipes = recipes.filter(tag_lunch=True)
    if 'tag_dinner' in tags:
        recipes = recipes.filter(tag_dinner=True)
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
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    )).annotate(is_purchase=Exists(
        PurchaseItem.objects.filter(
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    ))
    tags = request.GET.getlist('tag')
    if 'tag_breakfast' in tags:
        recipes = recipes.filter(tag_breakfast=True)
    if 'tag_lunch' in tags:
        recipes = recipes.filter(tag_lunch=True)
    if 'tag_dinner' in tags:
        recipes = recipes.filter(tag_dinner=True)
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
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    )).filter(is_favorite=True).annotate(is_purchase=Exists(
        PurchaseItem.objects.filter(
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    ))
    tags = request.GET.getlist('tag')
    if 'tag_breakfast' in tags:
        recipes = recipes.filter(tag_breakfast=True)
    if 'tag_lunch' in tags:
        recipes = recipes.filter(tag_lunch=True)
    if 'tag_dinner' in tags:
        recipes = recipes.filter(tag_dinner=True)
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
    users = USER.objects.filter(following__user=request.user).annotate(recipes_count=Count('recipes')).order_by(
        'username')
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
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient[0], count=ingredient[1])
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
    title = "Редактирование рецепта"
    save_button = "Сохранить"
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
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient[0], count=ingredient[1])
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
    recipe = Recipe.objects.filter(pk=recipe_id).annotate(is_favorite=Exists(
        Favorite.objects.filter(
            user_id=request.user.pk,
            recipe_id=recipe_id,
        ),
    )).annotate(is_purchase=Exists(
        PurchaseItem.objects.filter(
            user=request.user,
            recipe_id=OuterRef('pk'),
        ),
    ))[0]
    follow = Follow.objects.filter(user=request.user, author=recipe.author).exists()
    return render(
        request,
        "recipe.html",
        {"recipe": recipe, "follow": follow}
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
    content = f"Время {datetime.datetime.now()}\n" \
              f"Всего репептов - {recipes.count()}\n" \
              f"Список составлен для {full_name}\n" \
              "Ингридиенты:\n" + ingredients_in_text(items)
    filename = f"purchase_{request.user.username}.txt"
    response = HttpResponse(content, content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename={0}".format(filename)
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
