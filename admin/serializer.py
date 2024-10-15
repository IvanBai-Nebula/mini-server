from rest_framework import serializers

from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone', 'email', 'avatar')
        extra_kwargs = {
            'id': {'read_only': True, 'allow_null': True, 'required': False},
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
            'phone': {'allow_null': True, 'required': False},
            'email': {'required': True},
            'avatar': {'allow_null': True, 'required': False},
        }

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone', ''),
            avatar=validated_data.get('avatar', ''),
        )

        return user
