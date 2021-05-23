from django.contrib.auth import get_user_model
from django.db import models

USER = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    dimension = models.CharField(max_length=100, verbose_name='Единицы измерения')

    def __str__(self):
        return f"{self.title} {self.dimension}"

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    author = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name='Автор', related_name="recipes")
    text = models.TextField(verbose_name='Описание')
    time_cooking = models.PositiveIntegerField(verbose_name='Время приготовления', help_text='Время приготовления в минутах')
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient', through_fields=('recipe', 'ingredient'), verbose_name='Ингридиент')
    image = models.ImageField(upload_to='recipe/', verbose_name='Картинка', default=0)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tag_breakfast = models.BooleanField(verbose_name='Завтрак', default=False)
    tag_lunch = models.BooleanField(verbose_name='Обед', default=False)
    tag_dinner = models.BooleanField(verbose_name='Ужин', default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe_ingredients')
    count = models.PositiveIntegerField(verbose_name='Количество')


class Follow(models.Model):
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="follower",
    )
    author = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        verbose_name="Автор",
        related_name="following",
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(fields=["user", "author"],
                                    name="unique_follow"),
        ]

class Favorite(models.Model):
    user = models.ForeignKey(
        USER,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    def __str__(self):
        return f'Избранный {self.recipe} у {self.user}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite_user_recipe'
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

class PurchaseItem(models.Model):
    user = models.ForeignKey(
        USER,
        related_name='purchase',
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='purchase',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe', ],
                                    name='two_recipes_in_one_cart_impossible')
        ]
