from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet
from ingridients.views import IngredientViewSet
from tags.views import TagViewSet
from users.views import CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register('ingredients', IngredientViewSet)
router_v1.register('recipes', RecipeViewSet)
router_v1.register('tags', TagViewSet)
router_v1.register('users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_v1.urls)),
    path('api/auth/', include('djoser.urls.authtoken')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
    ),
    path(
        'redoc/openapi-schema.yml',
        TemplateView.as_view(template_name='openapi-schema.yml'),
    )
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
