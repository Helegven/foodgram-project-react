from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User


class MakeUserTest(APITestCase):
    def test_create_user(self):
        request_data = {
            'email': 'test@mail.com',
            'username': 'test',
            'firt_name': 'Dyadya',
            'last_name': 'Vitiya',
            'password': '1234!wowpassword'
        }
        response = self.client.post(reverse('api:users'), request_data)
        excepted_data = {
            'email': 'test@mail.com',
            'username': 'test',
            'firt_name': 'Dyadya',
            'last_name': 'Vitiya',
            'id': 1
        }
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED, "Ответ сервера не 201"
        )
        self.assertEqual(
            User.objects.count(),
            1,
            "Новый пользователь не появиился в Базе данных"
        )
        self.assertEqual(
            response.data,
            excepted_data,
            "Проверьте тело ответа на ошибку, несоотвествие документации"
        )
