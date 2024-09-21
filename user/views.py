import json
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.settings import api_settings
from .models import *
from .serializer import *


class AdminLoginView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        # 获取请求参数
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 验证用户是否存在
        try:
            user = User.objects.get(username=username)
            if user.password != password:
                return JsonResponse({'code': 401, 'success': 'false', 'msg': '用户名或密码错误'})

            if user.is_deleted:
                return JsonResponse({'code': 403, 'success': 'false', 'msg': '该用户已被删除'})

            if user.role.name == 'normal':
                return JsonResponse({'code': 403, 'success': 'false', 'msg': '该用户权限不足'})

            # 生成 JWT Token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return JsonResponse({'code': 200, 'success': 'true', 'token': token})

        except User.DoesNotExist:
            return JsonResponse({'code': 401, 'success': 'false', 'msg': '用户名或密码错误'})

        except AuthenticationFailed as e:
            return JsonResponse({'code': 401, 'success': 'false', 'msg': str(e)})


class UserInfoView(View):

    def get(self, request):
        user_id = request.GET.get('user_id')
        try:
            user_info = UserInfo.objects.get(user=user_id)
            return JsonResponse({'code': 200, 'success': 'true', 'data': UserInfoSerializer(user_info).data})
        except UserInfo.DoesNotExist:
            return JsonResponse({'code': 404, 'success': 'false', 'msg': '用户信息不存在'})


class TestView(View):

    def get(self, request):
        userList_obj = User.objects.all()
        print(userList_obj, type(userList_obj))
        userList_dict = userList_obj.values()
        print(userList_dict, type(userList_dict))
        userList = list(userList_dict)
        print(userList, type(userList))
        return JsonResponse({'code': 200, 'msg': 'success', 'data': userList})


class JwtTestView(View):

    def get(self, request):
        try:
            user = User.objects.get(username='Ivan', password='byfcjx')
            print("User found:", user)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            print("Payload:", payload)
            token = jwt_encode_handler(payload)
            print("Token:", token)
            return JsonResponse({'code': 200, 'token': token})
        except User.DoesNotExist:
            print("User does not exist")
