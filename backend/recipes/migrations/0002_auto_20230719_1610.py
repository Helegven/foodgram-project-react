# Generated by Django 2.2.28 on 2023-07-19 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredients',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipetags',
            options={'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterModelOptions(
            name='shoppingcart',
            options={'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
    ]
