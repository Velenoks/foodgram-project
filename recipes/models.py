from django.contrib.auth import get_user_model
from django.db import models


USER = get_user_model()


class Ingredient(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    unit = models.CharField(max_length=100, verbose_name='Единицы измерения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Recipe(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    user = models.ForeignKey(USER, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField(verbose_name='Описание')
    time_cooking = models.PositiveIntegerField(verbose_name='Время приготовления', help_text='Время приготовления в минутах')
    ingredient = models.ManyToManyField(Ingredient, through='RecipeIngredient', verbose_name='Ингридиент')
    image = models.ImageField(upload_to='recipe/', verbose_name='Картинка', default=0)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    tag_breakfast = models.BooleanField(verbose_name='Завтрак', default=False)
    tag_lunch = models.BooleanField(verbose_name='Обед', default=True)
    tag_dinner = models.BooleanField(verbose_name='Ужин', default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
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
        constraints = [
            models.UniqueConstraint(fields=["user", "author"],
                                    name="unique_follow"),
        ]
