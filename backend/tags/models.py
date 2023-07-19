from django.core.validators import RegexValidator
from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Название тега',
    )
    color = models.CharField(
        'Цветовой HEX-код',
        unique=True,
        max_length=7,
        validators=[
            RegexValidator(
                regex='^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
                message='Введенное значение не является цветом в формате HEX!'
            )
        ]
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Идентификатор тега',
        help_text='Идентификатор тега',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
