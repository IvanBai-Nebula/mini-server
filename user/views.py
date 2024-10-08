import json
import requests
from django.http import JsonResponse
from django.views import View
from rest_framework_jwt.settings import api_settings
from mini_server.settings import MEDIA_ROOT
from .models import User
from .serializer import *
from django.contrib.auth.hashers import make_password, check_password

APP_ID = 'wx1234567890abcdef'
APP_SECRET = '1234567890abcdef1234567890abcdef'

REQUEST_SOURCE_WEB = 'web'
REQUEST_SOURCE_MINIAPP = 'miniapp'


class UserLoginView(View):

    @staticmethod
    def post(request):
        if request.method == 'POST':
            request_source = request.headers.get('Request-Source')
            if request_source == REQUEST_SOURCE_WEB:
                return UserLoginView.handle_web_login(request)
            elif request_source == REQUEST_SOURCE_MINIAPP:
                return UserLoginView.handle_miniapp_login(request)

    @staticmethod
    def handle_web_login(request):
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"success": False, "msg": "用户名和密码不能为空", "data": {}})

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                token = UserLoginView.generate_token(user)
                return JsonResponse({"success": True, "data": {"token": token, "username": user.username,
                                                               "avatar": user.avatar}})
            else:
                return JsonResponse({"success": False, "msg": "用户名或密码有误", "data": {}})
        except User.DoesNotExist:
            return JsonResponse({"success": False, "msg": "当前用户未注册", "data": {}})

    @staticmethod
    def handle_miniapp_login(request):
        code = request.POST.get('code')
        if not code:
            return JsonResponse({"success": False, "msg": "code不能为空", "data": {}})

        try:
            url = ('https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={'
                   '}&grant_type=authorization_code').format(APP_ID, APP_SECRET, code)
            response = requests.get(url)
            data = response.json()

            openid = data.get('openid')
            if openid:
                user, created = User.objects.get_or_create(openid=openid, defaults={'username': openid, 'role': 2})
                token = UserLoginView.generate_token(user)
                msg = "新用户注册成功" if created else "登录成功"
                return JsonResponse({"success": True, "msg": msg, "data": {"token": token, "username": user.username,
                                                                           "avatar": user.avatar}})
            else:
                return JsonResponse({"success": False, "msg": "获取openid失败", "data": {}})
        except requests.exceptions.RequestException:
            return JsonResponse({"success": False, "msg": "微信服务器请求失败", "data": {}})
        except Exception as e:
            return JsonResponse({"success": False, "msg": str(e), "data": {}})

    @staticmethod
    def generate_token(user):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        return jwt_encode_handler(payload)
