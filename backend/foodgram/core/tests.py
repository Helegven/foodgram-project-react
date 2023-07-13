from http import HTTPStatus

from django.test import Client, TestCase


class ViewTestClass(TestCase):
    def setUp(self):
        self.client = Client()

    def test_error_page(self):
        """Проверка status_code для запроса с ошибкой."""
        response = self.client.get('/nonexist-page/').status_code
        self.assertEqual(response, HTTPStatus.NOT_FOUND)

    def test_error_page(self):
        """URL-адрес c ошибкой использует соответствующий шаблон."""
        response = self.client.get('/nonexist-page/')
        self.assertTemplateUsed(response, 'core/404.html')