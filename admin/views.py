from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from utils.constants import *
from utils.permissions import IsAdminUser
from .serializer import *


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data
    res = RES_Failed
    serializer = CustomUserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(RES_SUCCESS, status=201)
    if 'username' in serializer.errors:
        print('用户名已存在')
        res.update({'msg': '用户名已存在'})
    else:
        res.update({'msg': serializer.errors})
    return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    res = RES_Failed
    username = request.data['username']
    password = request.data['password']

    if not username or not password:
        res.update({'msg': '用户名或密码不能为空'})
        return Response(res, status=400)

    # 使用 Django 内置方法验证用户
    user = authenticate(username=username, password=password)

    if user is None:
        res.update({'msg': '用户名或密码错误'})
        return Response(res, status=401)

    try:
        # 生成 JWT 令牌
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)

        # 构造响应数据
        res = RES_SUCCESS
        res.update({
            'data': {
                'id': user.id,
                'token': token,
                'username': user.username,
                'avatar': user.avatar,
                'mobile': user.phone
            }
        })

        return Response(res, status=200)

    except Exception as e:
        res.update({'msg': str(e)})
    return Response(res, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def reset_password(request):
    data = request.data
    res = RES_Failed
    try:
        user = AdminUser.objects.get(username=request.user.username)
        old_password = user.password
        if check_password(data['old'], old_password):
            user.set_password(data['new'])
            user.save()
            res = RES_SUCCESS
            return Response(res)
        res.update({'msg': '旧密码错误'})
        return Response(res)
    except Exception as e:
        res.update({'msg': str(e)})
        return Response(res)
