from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = "__all__"


class UserInfoSerializer2(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ("nickname", "age", "height", "weight", "blood_pressure", "blood_sugar", "blood_fat", "sleep_quality")


class CollectionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collections
        fields = "__all__"


class BrowsingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BrowsingHistory
        fields = "__all__"


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = "__all__"


class ChatRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRecord
        fields = "__all__"
