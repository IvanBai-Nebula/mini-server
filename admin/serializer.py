from rest_framework import serializers

from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'phone', 'email', 'avatar')
        extra_kwargs = {
            'id': {'read_only': True, 'allow_null': True, 'required': False},
            'username': {'required': True},
            'password': {'write_only': True, 'required': True},
            'phone': {'allow_null': True, 'required': False},
            'email': {'required': True},
            'avatar': {'allow_null': True, 'required': False}
        }

    @staticmethod
    def validate_phone(value):
        if value and User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("该手机号已被使用")
        return value

    @staticmethod
    def validate_email(value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被使用")
        return value

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data.get('username'),
            password=validated_data.get('password'),
            email=validated_data.get('email'),
            phone=validated_data.get('phone', ''),
            avatar=validated_data.get('avatar', ''),
        )

        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance