from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestSignin(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@example.com',
            password='vG2joknXWrC4p-HU',
        )

    def setUp(self):
        self.url = reverse('auth:signin')

    def test_signin_success(self):
        data = {
            'email': 'test@example.com',
            'password': 'vG2joknXWrC4p-HU',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])
        self.assertTrue(response.data['user']['id'])

    def test_signin_failed_invalid_password(self):
        data = {
            'email': 'test@example.com',
            'password': 'invalid',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'])

    def test_signin_failed_invalid_email(self):
        data = {
            'email': 'invalid@example.com',
            'password': 'vG2joknXWrC4p-HU',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data['non_field_errors'])
