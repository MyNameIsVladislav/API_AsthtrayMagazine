from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from purse.models import PurseModel
from purse.serializers import WalletSerializers


class UserWalletView(APIView):
    """Баланс пользователя"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = get_object_or_404(PurseModel, user_id=request.user)
        serializer = WalletSerializers(queryset)
        return Response(serializer.data)
