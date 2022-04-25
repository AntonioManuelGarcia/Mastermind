from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.status import HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from django.urls import reverse
from model_bakery import baker
from .models import *


class TestUsersAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(
            username="admin", password="admin",
            email="admin@example.com"
        )
        cls.user_deactivated = User.objects.create(
            username="useroff", password="admin", is_active=False,
            email="useroff@example.com"
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.user.delete()
        cls.user_deactivated.delete()

    def test_user_login(self):
        response = self.client.post('/api/users/auth/login/',
                                    {'username': 'admin', 'password': 'admin'}, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_user_register(self):
        response = self.client.post('/api/users/auth/register/',
                                    {'username': 'admin2', 'email': 'admin@gmail.com',
                                     'password': '@dm1n1str@d0r', 'password2': '@dm1n1str@d0r'}, format="json")
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_user_register_can_login(self):
        response = self.client.post('/api/users/auth/register/',
                                    {'username': 'admin2', 'email': 'admin@gmail.com',
                                     'password': '@dm1n1str@d0r', 'password2': '@dm1n1str@d0r'}, format="json")
        response2 = self.client.post('/api/users/auth/login/',
                                     {'username': 'admin2', 'password': '@dm1n1str@d0r'}, format="json")
        self.assertEqual(response2.status_code, HTTP_200_OK)
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_user_deactivate_cant_login(self):
        response = self.client.post('/api/users/auth/login/',
                                    {'username': 'useroff', 'password': 'admin'}, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

