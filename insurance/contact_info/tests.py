from django.test import TestCase

class ModelsStorageTest(TestCase):
    def test_models_storage_load(self):
        company_info = {
            'name': 'AegisAuto',
            'email': 'contact_aegis@gmail.com',
            'phone': '+48-98-567-657',
            'address': 'ul. Kwiatowa 29 , Warsaw, Poland'
        }
            
        response = self.client.post('/contact_info/', data=company_info)
        self.assertContains(response, 'AegisAuto')
        self.assertContains(response, '+48-98-567-657')
        self.assertContains(response, 'contact_aegis@gmail.com')
        self.assertContains(response, 'ul. Kwiatowa 29 , Warsaw, Poland')
