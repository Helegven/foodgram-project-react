from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from ingridients.models import Ingredient

from .models import RecipeIngredients


def add_ingridient(ingredients, recipe):
    for ingredient in ingredients:
        amount = ingredient['amount']
        ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

        RecipeIngredients.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )


def get_shopping_cart(request):
    ingredients = (
        RecipeIngredients.objects.filter(
            recipe__in_shopping_list__user=request.user
        ).annotate(
            total_amount=Sum('amount')
        ).values_list(
            'ingredient__name',
            'total_amount',
            'ingredient__measurement_unit'
        )
    )
    buy_list_text = [
        '{} - {} {}.'.format(*ingredient) for ingredient in ingredients]
    response = HttpResponse(
        'Список покупок с сайта Foodgram:\n'
        + '\n'.join(buy_list_text),
        content_type='text/plain'
    )
    response['Content-Disposition'] = (
        'attachment; filename=shopping-list.txt'
    )
    return response
