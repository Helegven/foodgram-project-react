from django.contrib import admin

from .models import Favorite, Subscription


@admin.register(Favorite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Subscription)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('user', 'author',)
