from django.shortcuts import get_object_or_404

from .models import RecipeIngredients
from ingridients.models import Ingredient


def ingridient_list(ingredients, recipe):
    for ingredient in ingredients:
        amount = ingredient['amount']
        ingredient = get_object_or_404(Ingredient, pk=ingredient['id'])

        RecipeIngredients.objects.create(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
