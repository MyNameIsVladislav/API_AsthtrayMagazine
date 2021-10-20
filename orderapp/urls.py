from django.urls import path

from orderapp.views import PaymentView


app_name = 'orderapp'

urlpatterns = [
    path('/', PaymentView.as_view(), name='create_order')
]
