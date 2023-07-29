from api.pagination import CustomPagination
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import exceptions, status
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response

from .models import Subscription, User
from .serializers import SubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    pagination_class = CustomPagination

    @action(
        detail=False,
        methods=['GET'],
        serializer_class=SubscriptionSerializer,
        permission_classes=(IsAuthenticated, )
    )
    def subscriptions(self, request):
        user = self.request.user
        user_subscriptions = user.subscribes.all()
        authors = [item.author.id for item in user_subscriptions]
        queryset = User.objects.filter(pk__in=authors)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = self.get_serializer(paginated_queryset, many=True)

        return self.get_paginated_response(serializer.data)

    @action(
        detail=True,
        methods=['POST'],
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)
        if user == author:
            raise exceptions.ValidationError(
                'Подписка на самого себя запрещена.'
            )
        if Subscription.objects.filter(
            user=user,
            author=author
        ).exists():
            raise exceptions.ValidationError('Подписка уже оформлена.')

        Subscription.objects.create(user=user, author=author)
        serializer = self.get_serializer(author)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        user = self.request.user
        author = get_object_or_404(User, pk=id)

        if not Subscription.objects.filter(
            user=user,
            author=author
        ).exists():
            raise exceptions.ValidationError(
                'Подписка не была оформлена, либо уже удалена.'
            )
        Subscription.objects.get(user=user, author=author).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
