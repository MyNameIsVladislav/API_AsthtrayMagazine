from django.urls import path, include

from rest_framework import routers

from articleapp.views import ArticleViewSet, CommentsView, LikeView


app_name = 'articleapp.api'

router = routers.SimpleRouter()
router.register(r'', ArticleViewSet)


urlpatterns = [
    path('comment/', CommentsView.as_view(), name='comment'),
    path('like/', LikeView.as_view(), name='like'),
    path('', include(router.urls)),

]
