from django.test import TestCase
from rest_framework.test import APIClient


class TestPricingView(TestCase):
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

        self.not_admin_data = {
            "username": "other",
            "password": "1234",
            "is_superuser": False,
            "is_staff": True
        }

        self.not_admin_login_data = {
            "username": "other",
            "password": "1234"
        }
    
    def test_pricing_format_status_with_admin_user(self):
        client = APIClient()

        pricing_data = {
            "a_coefficient": 100,
	        "b_coefficient": 100
            }

        output_format_pricing_data = {
            "id": 1,
            "a_coefficient": 100,
            "b_coefficient": 100
            }

        # create admin user
        client.post('/api/accounts/', self.admin_data, format='json')

        # get token admin
        token = client.post('/api/login/', self.admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create pricing
        response = client.post('/api/pricings/', pricing_data, format='json')

        pricing = response.json()

        self.assertDictContainsSubset(pricing, output_format_pricing_data)
        self.assertEqual(pricing['id'], 1)
        self.assertEqual(response.status_code, 201)
    
    def test_pricing_format_status_without_admin_user(self):
        client = APIClient()

        pricing_data = {
            "a_coefficient": 100,
	        "b_coefficient": 100
            }

        output_format_pricing_data = {
            "id": 1,
            "a_coefficient": 100,
            "b_coefficient": 100
            }

        # create user
        client.post('/api/accounts/', self.not_admin_data, format='json')

        # get token user
        token = client.post('/api/login/', self.not_admin_login_data, format='json').json()['token']

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        # create pricing
        response = client.post('/api/pricings/', pricing_data, format='json')

        self.assertEqual(response.status_code, 401)