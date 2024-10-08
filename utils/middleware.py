from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings


class AuthRequired(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        # 定义白名单路径
        white_list = ["/user/login"]
        path = request.path

        # 检查是否处于开发环境，并允许所有请求
        if settings.DEBUG:
            return None

        # 检查路径是否在白名单内或以 "/resource" 开头
        if path not in white_list and not path.startswith("/resource"):
            token = request.META.get('HTTP_AUTHORIZATION')
            # 检查 Token 是否存在
            res = {'success': False}
            if not token:
                res.update({'msg': 'Token不存在！'})
                return Response(res)

            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                res.update({'msg': 'Token已过期！'})
                return Response(res)
            except InvalidTokenError:
                res.update({'msg': 'Token无效！'})
                return Response(res)
            except PyJWTError:
                res.update({'msg': 'Token解析失败！'})
                return Response(res)
        else:
            return None
