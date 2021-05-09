from django.contrib.auth import get_user_model
from django.db import models


USER = get_user_model()

class Tag(models.Model):
    title = models.CharField(max_length=20, verbose_name='Название')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Прием пищи'


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
    tag = models.ManyToManyField(Tag, verbose_name='Прием пищи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name='Количество')
