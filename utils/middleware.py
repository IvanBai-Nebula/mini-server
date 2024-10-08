from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings


class AuthRequired(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        # 定义白名单路径
        white_list = ["/user/login"]
        path = request.path

        # 检查路径是否在白名单内或以 "/resource" 开头
        if path not in white_list and not path.startswith("/resource"):
            token = request.META.get('HTTP_AUTHORIZATION')
            # 检查 Token 是否存在
            if not token:
                return HttpResponse({"success": False, "msg": "Token不存在！"})

            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                return HttpResponse({"success": False, "msg": "Token已过期,请重新登录！"})
            except InvalidTokenError:
                return HttpResponse({"success": False, "msg": "Token无效,请重新登录！"})
            except PyJWTError:
                return HttpResponse({"success": False, "msg": "Token解析失败,请重新登录！"})
        else:
            return None
