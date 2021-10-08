from django.db.models import Count, F
from django.db.models.functions import ExtractMonth, ExtractYear

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.serializers import HiddenField
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from django_filters.rest_framework import DjangoFilterBackend

from articleapp.filters import ArticleFilter
from articleapp.serializers import (
    ArticleSerializers,
    ArticleDetailSerializer,
    CommentCreateSerializer,
    LikeCreateSerializer,
)
from articleapp.models import ArticleModel, ModelLikesArticle


class ArticleViewSet(ReadOnlyModelViewSet):
    """Получение статей, статьи"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ArticleFilter
    queryset = ArticleModel.objects.all()
    serializer_class = ArticleSerializers
    lookup_field = 'pk'
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.annotate(
            likes=Count('articleapp_modellikesarticle')
        ).annotate(
            month=ExtractMonth('publish')
        ).annotate(
            year=ExtractYear('publish')
        ).filter(is_active=True)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ArticleDetailSerializer(instance)
        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='popular', url_name='popular')
    def popular(self, request, *args, **kwargs):
        queryset = ArticleModel.objects.all().annotate(
            likes=Count('articleapp_modellikesarticle', distinct=True)
        ).annotate(
            total_active=F('likes') + Count('articleapp_commentsmodel', distinct=True)
        ).order_by('-total_active')
        serializer = self.get_serializer(self.filter_queryset(queryset), many=True)
        return Response(serializer.data)


class CommentsView(CreateAPIView):
    """Оставить комментарий"""

    permission_classes = (IsAuthenticated,)
    serializer_class = CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.fields['user_id'] = HiddenField(default=request.user)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        headers['article_id'] = serializer.data['article_id']
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LikeView(APIView):
    """Поставить лайк"""

    authentication_classes = (BasicAuthentication, TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeCreateSerializer

    def put(self, request, *args, **kwargs):
        data, like_status = self.update_object(request, request.data)
        return Response(data, status=201, headers={
            'Like-status': like_status,
            'Name': request.user.userprofile.full_name
            }
        )

    @staticmethod
    def get_queryset_(pk):
        return ArticleModel.objects.get(pk=pk)

    def update_object(self, instance, data):
        query = self.get_queryset_(data['article_id'])
        obj, status_create = ModelLikesArticle.objects.get_or_create(user_id=instance.user, article_id=query)
        obj.status = False if not status_create and obj.status else True
        obj.save()
        return self.serializer_class(obj).data, obj.status
