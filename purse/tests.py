from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


User = get_user_model()


class CheckWalletTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email='test@test.com',
            password='password',
            birthday='1999-10-10'
        )
        self.token, status = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()

    def test_look_money(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.get('/api/wallet/user/')
        self.assertEqual(response.status_code, 200)

    def test_if_user_is_anon(self):
        response = self.client.get('/api/wallet/user/')
        self.assertEqual(response.status_code, 401)

