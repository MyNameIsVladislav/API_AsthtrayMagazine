from rest_framework import serializers

from shopapp.models import Product


class ProductSerializers(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Product
        exclude = ('available', 'created', 'updated')

