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

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('username','height','weight','birthday','pulse','blood_pressure','blood_sugar','blood_fat','user')
        extra_kwargs = {
            "username": {'allow_null': True, 'required': False},
            "height": {'allow_null': True, 'required': False},
            "weight": {'allow_null': True, 'required': False},
            "birthday": {'allow_null': True, 'required': False},
            "pulse": {'allow_null': True, 'required': False},
            "blood_pressure": {'allow_null': True, 'required': False},
            "blood_sugar": {'allow_null': True, 'required': False},
            "blood_fat": {'allow_null': True, 'required': False},
        }

    def create(self, validated_data):
        user = CustomerUser.objects.create_user(**validated_data)

        return user




