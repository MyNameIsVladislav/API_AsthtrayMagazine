from django.db.models import Count, F
from django.db.models.functions import ExtractMonth, ExtractYear
from rest_framework.decorators import action
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from articleapp.filters import ArticleFilter
from articleapp.serializers import ArticleSerializers, ArticleDetailSerializer
from articleapp.models import ArticleModel


class ArticleViewSet(ReadOnlyModelViewSet):
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
