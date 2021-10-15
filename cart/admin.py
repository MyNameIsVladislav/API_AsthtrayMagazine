from django.contrib import admin

from cart.models import BasketModel, BasketProductModel


admin.site.register(BasketModel)
admin.site.register(BasketProductModel)
