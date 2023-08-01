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
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)

    @admin.display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
