from django.test import TestCase
from rest_framework.test import APIClient
import ipdb

# Testar se somente o usuário autenticado pode criar um nível - OK
# Testar se um usuário não autenticado pode criar um nível - OK
# Testar se um nível que já exista é criado novamente
# Testar se o formato de saída é o esperado
# Testar se as vagas estão sendo preenchidas, ou seja, se o número de vagas disponíveis diminui quando os veículos entram.

class TestLevelView(TestCase):
    def setUp(self):
        self.admin_data = {
            "username": "admin",
            "password": "1234",
            "is_superuser": True,
            "is_staff": True
        }

        self.not_admin_data = {
            "username": "other",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True
        }

        self.admin_login_data = {
            "username": "admin",
            "password": "1234"
        }

        self.not_admin_login_data = {
            "username": "other",
            "password": "1234"
        }
    
    def test_create_level_not_admin(self):
        client = APIClient()
        level_data = {
            "name": "floor 8",
            "fill_priority": 2,
	        "bike_spots": 20,
	        "car_spots": 30
            }
        
        # sem autenticação devolve 401
        response = client.post('/api/levels/', level_data, format='json')

        self.assertEqual(response.status_code, 401)

        # create not admin user
        client.post('/api/accounts/', self.not_admin_data, format='json')

        # get not admin token
        token = client.post(
            '/api/login/', self.not_admin_login_data, format='json'
        ).json()['token']


        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level not admin
        response = client.post('/api/levels/', level_data, format='json')

        self.assertEqual(response.status_code, 401)

    def test_create_level_admin(self):
        client = APIClient()
        level_data = {
            "name": "floor 8",
            "fill_priority": 2,
	        "bike_spots": 20,
	        "car_spots": 30
            }
        
        # sem autenticação devolve 401
        response = client.post('/api/levels/', level_data, format='json')

        self.assertEqual(response.status_code, 401)

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get admin token
        token = client.post(
            '/api/login/', self.admin_login_data, format='json'
        ).json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level with admin credentials
        response = client.post('/api/levels/', level_data, format='json')

        level = response.json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(level['id'], 1)

    def test_create_two_level_with_the_same_name(self):
        client = APIClient()
        level_data = {
            "name": "floor 8",
            "fill_priority": 2,
	        "bike_spots": 20,
	        "car_spots": 30
        }

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get admin token
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create two levels with the same name with admin credentials
        response1 = client.post('/api/levels/', level_data, format='json')
        response2 = client.post('/api/levels/', level_data, format='json')

        level1 = response1.json()
        level2 = response2.json()

        self.assertEqual(response1.status_code, 201)
        self.assertEqual(response2.status_code, 201)
        self.assertEqual(level1['id'], 1)
        self.assertEqual(level2['id'], 1)

    def test_output_format_level(self):
        client = APIClient()

        level_data = {
            "name": "floor 8",
            "fill_priority": 2,
	        "bike_spots": 20,
	        "car_spots": 30
        }

        output_format_data = {
            "id": 1,
            "name": "floor 8",
            "fill_priority": 2,
            "available_spots": {
                "available_bike_spots": 20,
                "available_car_spots": 30
                }
        }
        
        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get admin login
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level with admin credentials
        response = client.post('/api/levels/', level_data, format='json')

        level = response.json()
        
        self.assertDictContainsSubset(level, output_format_data)

    def test_get_output_format_level(self):
        client = APIClient()

        level_data_1 = {
            "name": "floor 1",
            "fill_priority": 5,
	        "bike_spots": 20,
	        "car_spots": 50
        }

        level_data_2 = {
            "name": "floor 2",
            "fill_priority": 3,
	        "bike_spots": 10,
	        "car_spots": 30
        }

        output_format_data = [
            {
                "id": 1,
                "name": "floor 1",
                "fill_priority": 5,
                "available_spots": {
                    "available_bike_spots": 20,
                    "available_car_spots": 50
                    }
                },
            {
                "id": 2,
                "name": "floor 2",
                "fill_priority": 3,
                "available_spots": {
                    "available_bike_spots": 10,
                    "available_car_spots": 30
                    }
                }
            ]
        
        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get admin login
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create two level with admin credentials
        client.post('/api/levels/', level_data_1, format='json')
        client.post('/api/levels/', level_data_2, format='json')

        response = client.get('/api/levels/', format='json')

        level = response.json()
        
        self.assertListEqual(level, output_format_data)
        self.assertEqual(response.status_code, 200)