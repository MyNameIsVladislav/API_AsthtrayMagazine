from rest_framework import serializers

from purse.models import PurseModel


class WalletSerializers(serializers.ModelSerializer):
    user_id = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = PurseModel
        fields = ('user_id', 'full_name', 'money')
