# Generated by Django 3.2.2 on 2021-05-22 10:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0014_rename_title_ingredient_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='name',
            new_name='title',
        ),
    ]
