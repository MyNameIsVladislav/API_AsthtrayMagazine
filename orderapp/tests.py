from decimal import Decimal
from unittest import mock

from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from cart.models import BasketModel, BasketProductModel
from shopapp.models import Product, Category
from purse.models import PurseModel
from orderapp.views import PaymentView


User = get_user_model()


DATA = {
            'first_name': 'Test',
            'last_name': 'Tester',
            'address': 'Testovay 7',
            'postal_code': '123123',
            'city': 'Testgrad',
            'email': 'sergiodonatelydota2@gmail.com'
}


class MockWallet:
    money = Decimal(5000)

    def save(self):
        pass


class TestOrderCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='password',
            birthday='1999-10-10'
        )
        self.cart, _ = BasketModel.objects.get_or_create(user=self.user)
        category = Category.objects.create(name='cap', slug='cap')
        product = Product.objects.create(
            category=category,
            name='DICK',
            slug='dick',
            price=Decimal(3230.9),
            stock=12
        )
        item = BasketProductModel.objects.create(cart=self.cart, product=product, quantity=2)
        self.view = PaymentView.as_view()
        self.wallet, _ = PurseModel.objects.get_or_create(user_id=self.user)
        self.client = APIClient()
        self.factory = APIRequestFactory()

    def test_look_cart(self):
        request = self.factory.get('api/order/')
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, 200)

    def test_paid_order_false(self):
        response = self.response_user_auth()
        self.assertEqual(response.status_code, 202)

    def test_paid_order_true(self):
        mock_money = MockWallet()
        with mock.patch('orderapp.service.Payment._get_purse', return_value=mock_money) as mk:
            response = self.response_user_auth()
            self.assertEqual(response.status_code, 201)

    def response_user_auth(self):
        request = self.factory.post('api/order/', DATA)
        force_authenticate(request, user=self.user)
        return self.view(request)
