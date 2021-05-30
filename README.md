# Продуктовый помощник
![Action](https://github.com/Velenoks/foodgram-project/workflows/diplom_workflow/badge.svg)

http://pavel-zakharov.ru/ - по данному адресу можно проверить работу приложения

<h2>Продуктовый помощник</h2>

Это онлайн-сервис, где пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

<h2>Развертывание окружения</h2>

Для начала необходимо выполнить команду <code>docker-compose build</code>, произойдет сборка проекта.
Затем нужно запустить проект командой <code>docker-compose up</code>.

Для выполнения миграций выполните команду <br> <code>docker-compose exec web python manage.py migrate</code>

Для добавления ингредиентов в базу данных <br> <code>docker-compose exec web python manage.py load_ingredient</code>

Для сбора статки выполните команду <br> <code>docker-compose exec web python manage.py collectstatic --no-input</code>

Для создания суперпользователя выполните команду <br> <code>docker-compose exec web python manage.py createsuperuser</code>