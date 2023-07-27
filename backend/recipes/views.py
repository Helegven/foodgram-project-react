from api.filters import RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorOrAdminPermission
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from ingridients.models import Ingredient
from rest_framework import exceptions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Favorite

from .models import Recipe, RecipeIngredients, ShoppingCart
from .serializers import (RecipeCreateUpdateSerializer, RecipeSerializer,
                          ShortRecipeSerializer)
from .shop_cart import get_shopping_cart


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

    @action(detail=True, methods=['POST'])
    def favorite(self, request, pk=None):
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

    @favorite.mapping.delete
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

    @action(detail=True, methods=['POST'])
    def shopping_cart(self, request, pk=None):
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

    @shopping_cart.mapping.delete
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
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        try:
            return get_shopping_cart(request)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
