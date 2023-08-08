from django.contrib import admin

from .models import Recipe, ShoppingCart


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

    def added_in_favorites(self, obj):
        return obj.in_favorite.count()
    added_in_favorites.short_description = 'Количество в избранных'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
