from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from core.settings import AUTH_USER_MODEL
from shopapp.models import Product

from cart.tasks import del_product_in_cart


class BasketModel(models.Model):
    user = models.OneToOneField(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user',
        related_name='user_cart'
    )

    @property
    def total_cost(self):
        return sum(item.total_price for item in self.in_cart.all())


class BasketProductModel(models.Model):
    cart = models.ForeignKey(BasketModel, on_delete=models.CASCADE, verbose_name='cart', related_name='in_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='product')
    quantity = models.PositiveIntegerField(verbose_name='quantity')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @property
    def price(self):
        return self.product.price

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.cart.user.first_name} - {self.product.name} - {self.quantity}'


@receiver(post_save, sender=BasketProductModel)
def delete_old_product(sender, instance=None, created=False, **kwargs):
    time = int(timedelta(days=15).total_seconds())
    del_product_in_cart.apply_async((instance.pk,), countdown=time)
