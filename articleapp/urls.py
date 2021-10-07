from django.urls import path, include

from rest_framework import routers

from articleapp.views import ArticleViewSet


app_name = 'articleapp.api'

router = routers.SimpleRouter()
router.register(r'', ArticleViewSet)


urlpatterns = [
    path('', include(router.urls))
]
