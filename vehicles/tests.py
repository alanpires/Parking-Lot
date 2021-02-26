from django.test import TestCase
from rest_framework.test import APIClient
from .services import calculate_amount_paid
from datetime import datetime
import ipdb


class TestVehicleView(TestCase):
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

        self.level_data_1 = {
            "name": "floor 1",
            "fill_priority": 2,
	        "bike_spots": 1,
	        "car_spots": 2
            }

        self.level_data_2 = {
            "name": "floor 2",
            "fill_priority": 5,
	        "bike_spots": 1,
	        "car_spots": 1
            }

        self.level_data_3 = {
            "name": "floor 3",
            "fill_priority": 3,
	        "bike_spots": 1,
	        "car_spots": 1
            }
        
        self.level_data_4 = {
            "name": "floor 4",
            "fill_priority": 5,
	        "bike_spots": 1,
	        "car_spots": 1
            }

        self.vehicle_data_1 = {
                "vehicle_type": "car",
                "license_plate": "AYO1029"
                }
        
        self.vehicle_data_2 = {
                "vehicle_type": "car",
                "license_plate": "AYO1030"
                }

        self.vehicle_data_3 = {
                "vehicle_type": "bike",
                "license_plate": "AYO1031"
                }
        
        self.vehicle_data_4 = {
                "vehicle_type": "car",
                "license_plate": "AYO1031"
                }
        
        self.pricing_data = {
                "a_coefficient": 100,
	            "b_coefficient": 100
                }

    def test_vehicle_entry(self):
        client = APIClient()
        
        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level admin user
        level_1 = client.post('/api/levels/', self.level_data_1, format='json').json()
        level_2 = client.post('/api/levels/', self.level_data_2, format='json').json()
        level_3 = client.post('/api/levels/', self.level_data_3, format='json').json()

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # create vehicle entry
        response = client.post('/api/vehicles/', self.vehicle_data_1, format='json')
        vehicle = response.json()

        # get levels
        levels = client.get('/api/levels/', format='json').json()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(vehicle['id'], 1)
        self.assertEqual(levels[0]['available_spots']['available_car_spots'], 2)
        self.assertEqual(levels[1]['available_spots']['available_car_spots'], 0)
        self.assertEqual(levels[2]['available_spots']['available_car_spots'], 1)

    def test_vehicle_entry_without_created_level_but_with_pricing(self):
        client = APIClient()
        
        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # create vehicle entry
        response = client.post('/api/vehicles/', self.vehicle_data_1, format='json')

        # vehicle = response.json()
        self.assertEqual(response.status_code, 404)
    
    def test_vehicle_entry_without_created_pricing_but_with_level(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level
        client.post('/api/levels/', self.level_data_1, format='json')
        
        # create vehicle entry
        response = client.post('/api/vehicles/', self.vehicle_data_1, format='json')

        # vehicle = response.json()
        self.assertEqual(response.status_code, 404)

    def test_vehicle_entry_without_created_pricing_and_without_level(self):
        client = APIClient()
        
        # create vehicle entry
        response = client.post('/api/vehicles/', self.vehicle_data_1, format='json')

        # vehicle = response.json()
        self.assertEqual(response.status_code, 404)
    
    def test_vehicle_entry_with_level_but_without_available_spot(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get admin token
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create levels
        level_2 = client.post('/api/levels/', self.level_data_2, format='json').json()
        level_3 = client.post('/api/levels/', self.level_data_3, format='json').json()

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # create vehicle entry
        response_1 = client.post('/api/vehicles/', self.vehicle_data_1, format='json')
        response_2 = client.post('/api/vehicles/', self.vehicle_data_2, format='json')
        response_3 = client.post('/api/vehicles/', self.vehicle_data_4, format='json')

        # get levels
        levels = client.get('/api/levels/', format='json').json()

        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)
        self.assertEqual(response_3.status_code, 404)
        self.assertEqual(levels[0]['available_spots']['available_car_spots'], 0)
        self.assertEqual(levels[1]['available_spots']['available_car_spots'], 0)
    
    def test_vehicle_entry_with_two_levels_of_the_same_fill_priority(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create three levels being two of the same level
        level_1 = client.post('/api/levels/', self.level_data_1, format='json').json()
        level_2 = client.post('/api/levels/', self.level_data_2, format='json').json()
        level_4 = client.post('/api/levels/', self.level_data_4, format='json').json()

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # entry vehicle
        response_1 = client.post('/api/vehicles/', self.vehicle_data_1, format='json')

        # get levels
        levels = client.get('/api/levels/', format='json').json()

        self.assertEqual(levels[0]['available_spots']['available_car_spots'], 2)
        self.assertEqual(levels[1]['available_spots']['available_car_spots'], 0)
        self.assertEqual(levels[2]['available_spots']['available_car_spots'], 1)
        self.assertEqual(response_1.status_code, 201)

    
    def test_exit_vehicle_amount_paid(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level
        client.post('/api/levels/', self.level_data_1, format='json')

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # entry vehicle
        client.post('/api/vehicles/', self.vehicle_data_1, format='json')

        # exit vehicle
        response = client.put('/api/vehicles/1/', format='json')

        self.assertEqual(response.status_code, 200)
    
    def test_exit_vehicle_spot_null(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level
        client.post('/api/levels/', self.level_data_1, format='json')

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # entry vehicle
        client.post('/api/vehicles/', self.vehicle_data_1, format='json')

        # exit vehicle
        response = client.put('/api/vehicles/1/', format='json')

        exit_vehicle = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(exit_vehicle['spot'], None)
    
    def test_exit_vehicle_level_available_spots(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level
        client.post('/api/levels/', self.level_data_1, format='json')

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # entry vehicle
        client.post('/api/vehicles/', self.vehicle_data_1, format='json')
        client.post('/api/vehicles/', self.vehicle_data_2, format='json')

        # exit vehicle
        client.put('/api/vehicles/1/', format='json')

        # get levels
        levels = client.get('/api/levels/', format='json').json()
        
        self.assertEqual(levels[0]['available_spots']['available_car_spots'], 1)

    def test_exit_two_vehicle_level_available_spots(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level
        client.post('/api/levels/', self.level_data_1, format='json')

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # entry vehicle
        client.post('/api/vehicles/', self.vehicle_data_1, format='json')
        client.post('/api/vehicles/', self.vehicle_data_2, format='json')

        # exit vehicle
        client.put('/api/vehicles/1/', format='json')
        client.put('/api/vehicles/2/', format='json')

        # get levels
        levels = client.get('/api/levels/', format='json').json()
        
        self.assertEqual(levels[0]['available_spots']['available_car_spots'], 2)
        
    def test_exit_vehicle_with_invalid_id(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create level
        client.post('/api/levels/', self.level_data_1, format='json')

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # entry vehicle
        client.post('/api/vehicles/', self.vehicle_data_1, format='json')
        client.post('/api/vehicles/', self.vehicle_data_2, format='json')

        # exit vehicle
        client.put('/api/vehicles/1/', format='json')
        client.put('/api/vehicles/2/', format='json')
        response = client.put('/api/vehicles/3/', format='json')
        
        self.assertEqual(response.status_code, 404)

    def test_function_calculate_amount_paid(self):
        client = APIClient()

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin user
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create pricing
        client.post('/api/pricings/', self.pricing_data, format='json')

        # calculate function
        start = "2021-01-21T19:36:55.364610Z"
        end = "2021-01-21T19:37:23.016452Z"
        f = '%Y-%m-%dT%H:%M:%S.%fZ'

        value = calculate_amount_paid(datetime.strptime(start, f), datetime.strptime(end, f))

        self.assertEqual(value, 100)