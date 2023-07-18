from http import HTTPStatus

from django.shortcuts import render


def page_not_found(request, exception):
    """Ошибка 404 - страница не найдена"""
    return render(
        request, 'core/404.html', {'path': request.path}, HTTPStatus.NOT_FOUND
    )


def server_error(request):
    """Ошибка 500 - проблемы со стороны сервера"""
    return render(request, 'core/500.html', HTTPStatus.INTERNAL_SERVER_ERROR)


def permission_denied(request, exception):
    """Ошибка 403 - доступ запрещен """
    return render(request, 'core/403.html', HTTPStatus.FORBIDDEN)


def csrf_failure(request, reason=''):
    """Ошибка 403 - утрачен токен csrf """
    return render(request, 'core/403csrf.html', HTTPStatus.FORBIDDEN)
