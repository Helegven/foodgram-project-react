from distutils.util import strtobool
from django_filters import rest_framework
from django_filters.rest_framework import filters

from recipes.models import Recipe, ShoppingCart
from tags.models import Tag
from users.models import Favorite


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = filters.BooleanFilter(
        method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )
    author = rest_framework.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited')

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorites__user=user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(in_shopping_list__user=user)
        return queryset

    # def filter_is_favorited(self, queryset, name, value):
    #     if self.request.user.is_anonymous:
    #         return Recipe.objects.none()

    #     favorites = Favorite.objects.filter(user=self.request.user)
    #     recipes = [item.recipe.id for item in favorites]
    #     new_queryset = queryset.filter(id__in=recipes)

    #     if not strtobool(value):
    #         return queryset.difference(new_queryset)

    #     return queryset.filter(id__in=recipes)

    # def filter_is_in_shopping_cart(self, queryset, name, value):
    #     if self.request.user.is_anonymous:
    #         return Recipe.objects.none()

    #     shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
    #     recipes = [item.recipe.id for item in shopping_cart]
    #     new_queryset = queryset.filter(id__in=recipes)

    #     if not strtobool(value):
    #         return queryset.difference(new_queryset)

    #     return queryset.filter(id__in=recipes)
