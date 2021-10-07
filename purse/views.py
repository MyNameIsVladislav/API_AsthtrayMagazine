from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from purse.models import PurseModel
from purse.serializers import WalletSerializers


class UserWalletView(APIView):

    def get(self, request):
        queryset = get_object_or_404(PurseModel, user_id=request.user)
        serializer = WalletSerializers(queryset)
        return Response(serializer.data)
