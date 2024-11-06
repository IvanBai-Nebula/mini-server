from rest_framework import serializers
from .models import *


class InfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Info
        fields = ('id', 'patient_name', 'birthday', 'gender', 'height', 'weight'
                  , 'pulse', 'blood_pressure', 'blood_sugar', 'blood_fat', 'user')
        extend_fields = {
            "id": {'allow_null': True, 'required': False},
            "patient_name": {'allow_null': True, 'required': False},
            "birthday": {'allow_null': True, 'required': False},
            "gender": {'allow_null': True, 'required': False},
            "height": {'allow_null': True, 'required': False},
            "weight": {'allow_null': True, 'required': False},
            "pulse": {'allow_null': True, 'required': False},
            "blood_pressure": {'allow_null': True, 'required': False},
            "blood_sugar": {'allow_null': True, 'required': False},
            "blood_fat": {'allow_null': True, 'required': False},
        }

    def create(self, validated_data):
        return Info.objects.create(**validated_data)
