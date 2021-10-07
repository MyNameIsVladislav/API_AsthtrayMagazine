from django_filters import rest_framework as filters

from shopapp.models import Product


class BaseFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    category = BaseFilter(field_name='category__name', lookup_expr='in')
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = ('category', 'price')
