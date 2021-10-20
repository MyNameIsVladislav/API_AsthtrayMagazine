from rest_framework import serializers

from orderapp.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()

    class Meta:
        model = Order
        exclude = ('created', 'updated', 'paid')
