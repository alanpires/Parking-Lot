from django.test import TestCase
from .models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.admin_data = {
            "username": "admin",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True
        }

    def test_create_user(self):
        admin = User.objects.create_user(**self.admin_data)
        # recarregar o usuário

        admin = User.objects.first()

        self.assertEqual(admin.username, self.admin_data['username'])
        self.assertEqual(admin.is_superuser, self.admin_data['is_superuser'])
        self.assertEqual(admin.is_staff, self.admin_data['is_staff'])
