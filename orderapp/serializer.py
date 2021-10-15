from rest_framework import serializers

from orderapp.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_name = serializers.CharField(max_length=30, default=serializers.CurrentUserDefault())
    last_name = serializers.CharField(max_length=50, default=serializers.CurrentUserDefault())
    email = serializers.EmailField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        exclude = ('created', 'updated', 'paid')

    def validate_first_name(self, value):
        if not isinstance(value, str):
            value = value.first_name
        return value

    def validate_last_name(self, value):
        if not isinstance(value, str):
            value = value.last_name
        return value

    def validate_email(self, value):
        if not isinstance(value, str):
            value = value.email
        return value

