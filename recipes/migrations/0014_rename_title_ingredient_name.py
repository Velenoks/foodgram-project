# Generated by Django 3.2.2 on 2021-05-22 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0013_alter_recipe_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='title',
            new_name='name',
        ),
    ]
