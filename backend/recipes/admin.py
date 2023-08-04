from django.contrib import admin

from .models import Recipe, ShoppingCart

if not hasattr(admin, "display"):
    """так-как у меня стоит устаревшая версия джанги,
    этот костыль имитируют работу декоратора displey """
    def display(description):
        def decorator(fn):
            fn.short_description = description
            return fn
        return decorator
    setattr(admin, "display", display)


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    min_num = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipe.tags.through
    extra = 1
    min_num = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'text',
        'pub_date',
        'author',
        'added_in_favorites'
    )
    search_fields = ('name', 'author')
    readonly_fields = ('added_in_favorites',)
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)

    @admin.display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.in_favorite.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
