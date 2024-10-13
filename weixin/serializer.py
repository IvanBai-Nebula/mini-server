from rest_framework import serializers

from .models import *


class WechatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = WechatUser
        fields = ('openid', 'username', 'phone', 'avatar')
        extra_kwargs = {
            "openid": {"required": True},
            "username": {"allow_null": True},
            "phone": {"allow_null": True, "required": False},
            "avatar": {"allow_null": True, "required": False}
        }

    def create(self, validated_data):
        user = WechatUser.objects.create_user({
            'openid': validated_data.get('openid'),
            'username': validated_data.get('username'),
            'phone': validated_data.get('phone', ''),
            'avatar': validated_data.get('avatar', ''),
        })

        return user
