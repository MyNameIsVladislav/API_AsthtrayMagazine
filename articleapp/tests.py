from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test.client import Client
from django.core.management import call_command

from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate

from articleapp.models import ArticleModel
from articleapp.views import CommentsView, LikeView


User = get_user_model()


class ArticlesTestCases(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.user = User.objects.create(
                email='test@test.com',
                password='password',
                birthday='1999-10-10'
            )
        self.client = Client()
        self.factory = APIRequestFactory()

    def test_articles_api(self):
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get('/api/articles/popular/')
        self.assertEqual(response.status_code, 200)

        for article in ArticleModel.objects.all():
            response = self.client.get(f'/api/articles/{article.id}/')
            self.assertEqual(response.status_code, 200)

    def test_add_comment(self):
        view = CommentsView.as_view()
        request = self.factory.post('api/articles/comment/', {'article_id': ['1'], 'text': ['NICE DICK']})
        self.auth_method(request, view)

    def test_add_like(self):
        view = LikeView.as_view()
        request = self.factory.put('api/articles/like/', {'article_id': ['1']})
        self.auth_method(request, view)

    def auth_method(self, request, view):
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        call_command('sqlsequencereset', 'articleapp', 'authapp')
