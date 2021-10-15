from rest_framework import serializers

from cart.models import BasketModel, BasketProductModel


class AddProductSerializers(serializers.ModelSerializer):
    cart = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BasketProductModel
        fields = ('product', 'quantity', 'cart')

    def validate_cart(self, value):
        return value.user_cart


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketProductModel
        fields = ['product', 'quantity', 'price', 'total_price']


class ProductInCartSerializer(serializers.ModelSerializer):
    in_cart = ItemSerializer(read_only=True, many=True)

    class Meta:
        model = BasketModel
        fields = ['user', 'in_cart']
