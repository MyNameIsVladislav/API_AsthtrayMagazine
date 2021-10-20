from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.management import call_command

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from cart.models import BasketModel
from cart.views import BasketProductView, UserCartView

User = get_user_model()


class CheckWalletTestCase(TestCase):

    def setUp(self) -> None:
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.user = User.objects.create(
            email='test@test.com',
            password='password',
            birthday='1999-10-10'
        )
        self.cart = BasketModel.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_add_product_in_cart(self):
        view = BasketProductView.as_view()
        data = {'product': ['1'], 'quantity': ['2']}
        request = self.factory.post('/api/cart/product/', data)
        self.check_auth(request, view, 201)

    def test_look_cart(self):
        view = UserCartView.as_view()
        request = self.factory.get('/api/cart/user')
        self.check_auth(request, view, 200)

    def check_auth(self, request, view, code):
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, code)
