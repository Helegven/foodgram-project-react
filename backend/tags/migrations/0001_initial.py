# Generated by Django 4.2.3 on 2023-08-03 13:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Название тега",
                        max_length=200,
                        verbose_name="Название тега",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        max_length=7,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Введенное значение не является цветом в формате HEX!",
                                regex="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$",
                            )
                        ],
                        verbose_name="Цветовой HEX-код",
                    ),
                ),
                (
                    "slug",
                    models.SlugField(
                        help_text="Идентификатор тега",
                        unique=True,
                        verbose_name="Идентификатор тега",
                    ),
                ),
            ],
            options={"verbose_name": "Тег", "verbose_name_plural": "Теги",},
        ),
    ]
