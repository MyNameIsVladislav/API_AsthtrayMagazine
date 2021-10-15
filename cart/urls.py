from django.urls import path, include

from cart.views import AddProductInCart, UserCartView

app_name = 'cart'

urlpatterns = [
    path('add-to-cart/', AddProductInCart.as_view(), name='add_to_cart'),
    path('user-cart/', UserCartView.as_view(), name='user-cart')
]
