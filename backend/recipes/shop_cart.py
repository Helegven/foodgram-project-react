from django.db.models import Sum
from django.http import HttpResponse

from .models import RecipeIngredients


def get_shopping_cart(request):
    ingredients = (
        RecipeIngredients.objects.filter(
            recipe__in_shopping_list__user=request.user
        ).values('ingredient').annotate(
            total_amount=Sum('amount')
            ).values_list('ingredient__name',
                          'total_amount',
                          'ingredient__measurement_unit'
                          )
    )
    buy_list_text = []
    [buy_list_text.append(
        '{} - {} {}.'.format(*ingredient)) for ingredient in ingredients]
    response = HttpResponse('Список покупок с сайта Foodgram:\n'
                            + '\n'.join(buy_list_text),
                            content_type='text/plain'
                            )
    response['Content-Disposition'] = (
        'attachment; filename=shopping-list.txt'
        )
    return response
