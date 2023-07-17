# import pytest
# from django.test import TestCase
# from rest_framework.test import APIRequestFactory, APIClient, force_authenticate


# @pytest.fixture
# def api_client():
#     return APIClient


# class TestIngredientsEndpoints:
#     """Тестирвоание эндпоинта"""

#     endpoint = "/api/v1/ingredients"

#     def test_igredients_get(self, endpoint, ingridient_factory):
#         response = api_client().get(self.endpoint)
#         assert response.status_code == 200



# class TestAPIEndpoints:

#     def setUp(self):
#         usert_test1 = User.obj

# factory = APIRequestFactory()
# user = User.objects.get(username='olivia')
# view = AccountDetail.as_view()

# # Make an authenticated request to the view...
# request = factory.get('/accounts/django-superstars/')
# force_authenticate(request, user=user)
# response = view(request)
