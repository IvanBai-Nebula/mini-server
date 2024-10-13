# tokens.py
from rest_framework_simplejwt.tokens import RefreshToken

from weixin.models import CustomerUser


class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user):
        user_id_field = 'openid' if isinstance(user, CustomerUser) else 'id'
        user_id = getattr(user, user_id_field)
        token = super().for_user(user)
        return token
