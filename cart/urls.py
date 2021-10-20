from django.urls import path, include

from cart.views import BasketProductView, UserCartView

app_name = 'cart'

urlpatterns = [
    path('product/', BasketProductView.as_view(), name='add_to_cart'),
    path('user/', UserCartView.as_view(), name='user-cart')
]
