# Generated by Django 2.2.28 on 2023-07-19 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название ингредиента', max_length=200, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='Единица измерения ингредиента', max_length=10, verbose_name='Единица измерения ингредиента')),
            ],
            options={
                'verbose_name': 'ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.AddConstraint(
            model_name='ingredient',
            constraint=models.UniqueConstraint(fields=('name', 'measurement_unit'), name='unique_ingredient'),
        ),
    ]