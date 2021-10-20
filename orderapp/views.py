from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from rest_framework.response import Response

from cart.serializers import ProductInCartSerializer
from cart.models import BasketModel

from orderapp.serializer import OrderSerializer
from orderapp.service import Payment


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        obj, _ = BasketModel.objects.get_or_create(user=request.user)
        serializer = ProductInCartSerializer(obj, context={'request': request, 'name': request.user.first_name})
        return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        cart = request.user.user_cart
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid() and cart.in_cart.all():
            return Payment.pay_product(request, serializer, cart)
        return Response(data={'Error': 'Заказ не может быть обработан'}, status=203)
