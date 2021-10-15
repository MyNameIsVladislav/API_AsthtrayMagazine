from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from cart.serializers import ProductInCartSerializer
from cart.models import BasketModel

from orderapp.serializer import OrderSerializer
from orderapp.service import pay_product


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        queryset = BasketModel.objects.get(user=request.user)
        serializer = ProductInCartSerializer(queryset, context={'request': request, 'name': request.user.first_name})
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        cart = request.user.user_cart
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid()
        if cart.in_cart.all():
            return pay_product(request, serializer, cart)
        return Response(data={'Error': 'Заказ не может быть обработан'}, status=203)
