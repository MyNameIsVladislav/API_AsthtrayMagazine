from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from cart.models import BasketProductModel, BasketModel
from cart.serializers import AddProductSerializers, ProductInCartSerializer


class AddProductInCart(UpdateModelMixin, CreateAPIView):
    queryset = BasketProductModel
    serializer_class = AddProductSerializers
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if (instance := BasketProductModel.objects.filter(
                cart__user=request.user, product__pk=int(request.data['product']))):
            return self.update(request, queryset=instance.first())

        return super(AddProductInCart, self).create(request, *args, **kwargs)

    def update(self, request, **kwargs):
        serializer = self.get_serializer(kwargs['queryset'], data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class UserCartView(APIView):
    """Баланс пользователя"""
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = get_object_or_404(BasketModel, user=request.user)
        serializer = ProductInCartSerializer(queryset)
        return Response(serializer.data)
