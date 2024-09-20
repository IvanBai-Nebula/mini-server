from rest_framework import serializers
from .models import *


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question
        fields = "__all__"
