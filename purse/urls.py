from django.urls import path

from purse.views import UserWalletView
app_name = 'purse'

urlpatterns = [
    path('user/', UserWalletView.as_view(), name='wallet')
]
