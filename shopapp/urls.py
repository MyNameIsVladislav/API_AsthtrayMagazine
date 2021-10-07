from django.urls import path, include

from rest_framework import routers

from shopapp.views import ProductsViewSet


app_name = 'shopapp'

router = routers.SimpleRouter()
router.register(r'', ProductsViewSet)

urlpatterns = [
    path('', include(router.urls))
]
