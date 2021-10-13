from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from shopapp.filters import ProductFilter
from shopapp.serializer import ProductSerializers
from shopapp.models import Product


class ProductsViewSet(ReadOnlyModelViewSet):
    """Просмотр товаров/товара"""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    lookup_field = 'pk'
    permission_classes = (IsAuthenticatedOrReadOnly,)
