from rest_framework import serializers

from .models import *


class CustomerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerUser
        fields = ('id', 'username', 'phone', 'avatar')
        extra_kwargs = {
            "id": {'required': True},
            "username": {'allow_null': True, 'required': False},
            "phone": {'allow_null': True, 'required': False},
            "avatar": {'allow_null': True, 'required': False}
        }

    def create(self, validated_data):
        user = CustomerUser.objects.create_user(**validated_data)

        return user
