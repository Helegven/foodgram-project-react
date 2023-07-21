from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.filters import RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrAdminPermission
from ingridients.models import Ingredient
from users.models import Favorite

from .models import Recipe, RecipeIngredients, ShoppingCart
from .serializers import (RecipeCreateUpdateSerializer, RecipeSerializer,
                          ShortRecipeSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrAdminPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateUpdateSerializer

        return RecipeSerializer

    @action(detail=True, methods=('post', 'delete'))
    def add_favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise exceptions.ValidationError('Рецепт уже в избранном.')

        Favorite.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('delete'))
    def del_favorite(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if not Favorite.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепта нет в избранном, либо он уже удален.'
            )

        favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
        favorite.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=('post'))
    def add_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)

        if ShoppingCart.objects.filter(
            user=user,
            recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                'Рецепт уже в списке покупок.'
            )

        ShoppingCart.objects.create(user=user, recipe=recipe)
        serializer = ShortRecipeSerializer(
            recipe,
            context={'request': request}
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('delete'))
    def del_shopping_cart(self, request, pk=None):
        user = self.request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if not ShoppingCart.objects.filter(
                user=user,
                recipe=recipe
        ).exists():
            raise exceptions.ValidationError(
                    'Рецепта нет в списке покупок, либо он уже удален.'
                )

        shopping_cart = get_object_or_404(
            ShoppingCart,
            user=user,
            recipe=recipe
        )
        shopping_cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=('get',),
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_cart]
        buy_list = RecipeIngredients.objects.filter(
            recipe__in=recipes
        ).values(
            'ingredient'
        ).annotate(
            amount=Sum('amount')
        )

        buy_list_text = 'Список покупок с сайта Foodgram:\n\n'
        for item in buy_list:
            ingredient = Ingredient.objects.get(pk=item['ingredient'])
            amount = item['amount']
            buy_list_text += (
                f'{ingredient.name}, {amount} '
                f'{ingredient.measurement_unit}\n'
            )

        response = HttpResponse(buy_list_text, content_type="text/plain")
        response['Content-Disposition'] = (
            'attachment; filename=shopping-list.txt'
        )

        return response
