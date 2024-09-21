from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings


class AuthRequired(MiddlewareMixin):

    def process_request(self, request):
        # 定义白名单路径
        white_list = ["/user/admin/login"]
        path = request.path

        # 检查路径是否在白名单内或以 "/storage" 开头
        if path not in white_list and not path.startswith("/storage"):
            print('要验证')
            token = request.META.get('HTTP_AUTHORIZATION')
            print("token:", token)

            # 检查 Token 是否存在
            if not token:
                return HttpResponse('缺少 Authorization 头！')

            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_decode_handler(token)
            except ExpiredSignatureError:
                return HttpResponse('Token过期，请重新登录！')
            except InvalidTokenError:
                return HttpResponse('Token验证失败！')
            except PyJWTError:
                return HttpResponse('Token验证异常！')
        else:
            print("不需要验证")
            return None
