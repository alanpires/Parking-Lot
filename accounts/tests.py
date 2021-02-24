from django.test import TestCase
from .models import User
from rest_framework.test import APIClient
import ipdb


class TestUserModel(TestCase):
    def setUp(self):
        self.admin_data = {
            "username": "admin",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True
        }

        self.admin_login_data = {
            "username": "admin",
            "password": "1234"
        }

    def test_create_user(self):
        admin = User.objects.create_user(**self.admin_data)
        
        # recarregar o usuário
        admin = User.objects.first()

        self.assertEqual(admin.username, self.admin_data['username'])
        self.assertEqual(admin.is_superuser, self.admin_data['is_superuser'])
        self.assertEqual(admin.is_staff, self.admin_data['is_staff'])
    
    def test_admin_login(self):
        client = APIClient()

        #login sem o usuário estar cadastrado, retorna 401
        response = client.post('/api/login/', self.admin_login_data, format='json')
        self.assertEqual(response.status_code, 401)

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # Usuário criado, retorna 200
        response = client.post('/api/login/', self.admin_login_data, format='json')
        self.assertEqual(response.status_code, 200)

        # get token
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        # usuário autenticado
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)