from django.conf import settings
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=settings.MAX_LEN,
        verbose_name='Название ингредиента',
        help_text='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единица измерения ингредиента',
        help_text='Единица измерения ингредиента',
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_ingredient'
            ),
        )

    def __str__(self):
        return self.name
