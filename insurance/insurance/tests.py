from django.test import TestCase
from django.core import mail

from .aihelper import ModelsStorage, insurance_types

class ModelsStorageTest(TestCase):
    def test_models_storage_load(self):
        storage = ModelsStorage() # create a clean one
        self.assertIsNone(storage.models)
        storage.ensure_loaded() # make sure it does not throw
        tmp_storage_models = storage.models
        self.assertSetEqual(set(storage.models.keys()), {'preprocessor'} | set(insurance_types))
        storage.ensure_loaded()
        self.assertIs(storage.models, tmp_storage_models)

class SupportViewTest(TestCase):
    def test_sends_email(self):
        data = {
            'name': 'Andrew',
            'email': 'andreww@test.net',
            'message': 'Testing the support sending'
        }
        self.client.post("/support/", data=data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(data['message'], mail.outbox[0].body)

class InsurancePricingViewTest(TestCase):
    def test_emits_result(self):
        form_data = {
            'first_name': 'Andrew',
            'last_name': 'White',
            'gender': 'male',
            'age': '28',
            'marital_status': 'married',
            'children': '0',
            'income': '7000',
            'employment': 'unemployed',
            'disability': 'on',
            'make': 'Honda',
            'model': 'Civic',
            'year': '2005',
            'fuel_type': 'Petrol',
            'engine_power': '200',
            'body_type': 'Sedan',
            'engine_volume': '1200',
            'driving_experience': '5',
            'vehicles_in_family': '1',
            'accidents': '0',
            'mileage': '20000',
            'vehicle_accidents': '1',
            'market_value': '25000',
            'total_owners': '2',
            'dashcam': 'on',
        }
        response = self.client.post('/insurance-pricing/', data=form_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')