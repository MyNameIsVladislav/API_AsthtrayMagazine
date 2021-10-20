from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from shopapp.models import Product


class ProductTestCase(TestCase):

    def setUp(self) -> None:
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()

    def test_products_api(self):
        response = self.client.get('/api/shop/')
        self.assertEqual(response.status_code, 200)

        for prod in Product.objects.all():
            response = self.client.get(f'/api/shop/{prod.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self) -> None:
        call_command('sqlsequencereset', 'shopapp', 'authapp')
