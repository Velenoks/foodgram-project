# Generated by Django 3.2.2 on 2021-05-23 09:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0017_auto_20210522_2237'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to='recipes.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.AddConstraint(
            model_name='purchaseitem',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='two_recipes_in_one_cart_impossible'),
        ),
    ]
