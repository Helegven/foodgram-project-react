from django.db.models import Sum
from django.http import HttpResponse

from ingridients.models import Ingredient

from .models import RecipeIngredients, ShoppingCart


def get_shopping_cart(request):
    shopping_cart = ShoppingCart.objects.filter(user=request.user)
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
