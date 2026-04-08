from django.contrib.auth import get_user_model
from django.test import TestCase

from ..serializers import UserSerializer

User = get_user_model()


class TestUserSerializer(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.exist_user = User.objects.create_user(
            email='exist@example.com',
            password='vG2joknXWrC4p-HU',
        )
        cls.exist_user.username = 'exist'
        cls.exist_user.save()

    def test_output_data(self):
        serializer = UserSerializer(instance=self.exist_user)
        expected_data = {
            'id': str(self.exist_user.id),
            'email': self.exist_user.email,
            'username': self.exist_user.username,
            'type': None,
        }
        self.assertDictEqual(serializer.data, expected_data)
