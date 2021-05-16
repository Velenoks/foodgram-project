from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=150,
                                blank=False,
                                verbose_name='Имя')
    last_name = models.CharField(max_length=150,
                                blank=False,
                                verbose_name='Фамилия')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
