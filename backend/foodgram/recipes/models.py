from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.html import format_html

User = get_user_model()


class Tag(models.Model):
    """Тэг"""

    name = models.CharField(
        max_length=200,
        unique=True,
        blank=True,
        null=True,
        verbose_name='Тег'
    )
    hexcolor = models.CharField(
        max_length=7,
        default="#ffffff",
        unique=True,
        blank=True,
        null=True
    )
    slug = models.SlugField(
        max_length=10,
        unique=True
    )

    def colored_name(self):
        return format_html(
            '<span style="color: #{};">{}</span>',
            self.hexcolor,
        )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} (цвет: {self.color})'


class Ingredient(models.Model):
    """Игридиенты для блюд"""

    name = models.CharField(
        max_length=200,
        verbose_name='Название ингридиента'
    )
    measurement_unit = models.CharField(
        max_length=10,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепты блюд"""

    author = models.ForeignKey(
        User,
        blank=True,
        null=True,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='author'
    )
    title = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Заголовок',
        help_text='Название блюда'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='recipes/',
        blank=True,
        null=True
    )
    description = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientsRecipes',
        related_name='ingredient',
        verbose_name='list ingredients',
        help_text='Список ингредиентов',
    )
    tags = models.ManyToManyField(
        Tag, through='TagsRecipe',
        related_name='recipes',
        help_text='Выберите тэг',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепты'

    def __str__(self):
        return self.description[:15]


class Comment(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Рецепт'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Коментарий'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )

    class Meta:
        verbose_name_plural = 'Коментарии'
        verbose_name = 'Коментарий'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        UniqueConstraint(
            fields=[
                'user',
                'author'
            ],
            name='uniq_follower'
        )
        verbose_name_plural = 'Подписки'
        verbose_name = 'Подписка'

    def __str__(self):
        return f'{self.user} подписался на {self.author}'
