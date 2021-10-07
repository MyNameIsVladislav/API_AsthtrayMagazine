from django_filters import rest_framework as filters

from articleapp.models import ArticleModel


class BaseFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ArticleFilter(filters.FilterSet):
    genres = BaseFilter(field_name='genres_id__name', lookup_expr='in')
    month = filters.RangeFilter()
    year = filters.RangeFilter()

    class Meta:
        model = ArticleModel
        fields = ('genres_id', 'month', 'year')
