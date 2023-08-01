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
