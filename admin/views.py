import random
import string
from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from utils.constants import *
from utils.permissions import IsAdminUser
from .serializer import *


@api_view(['POST'])
@permission_classes([AllowAny])
def send_email_captcha_view(request):
    """
    发送邮箱验证用于注册、密码重置
    :param request: {'email':'string'}
    :return: {'success':true|false, 'msg':'error'}
    """

    email = request.data['email']
    res = RES_Failed

    if not email:
        res.update({'msg': '邮箱不能为空'})
        return Response(res)

    captcha = ''.join(random.sample(string.digits, 6))
    try:
        message = f"""
        尊敬的用户，

        您好！您正在尝试注册/重置密码。
        您的验证码为：{captcha}，有效期为10分钟，请勿告知他人。
        请注意，此验证码仅在接下来的10分钟内有效。
        如有任何疑问，请联系客服。
        祝您使用愉快！

        照护者系统团队
        """

        send_mail("照护者后台注册验证码", message=message,
                  recipient_list=[email], from_email=None)

        # TODO: 后期用缓存实现存储验证码，这里目前使用session

        request.session['captcha'] = captcha
        request.session.set_expiry(timedelta(minutes=10).total_seconds())

        res = RES_SUCCESS
        return Response(res)
    except Exception as e:
        res.update({'msg': str(e)})
        return Response(res)


def verify_captcha(request):
    res = RES_Failed

    user_captcha = request.data['captcha']
    stored_captcha = request.session.get('captcha')

    if stored_captcha is None:
        res.update({'msg': '验证码已过期'})
        return Response(res)

    if user_captcha != stored_captcha:
        res.update({'msg': '验证码错误'})
        return Response(res)
    else:
        del request.session['captcha']

    return None


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    后台管理员注册（开发试用）
    :param request: {'username':'string', 'password':'string', 'email':'string', 'captcha':'string'}
    :return: {'success':true|false, 'msg':'error'}
    """

    param = request.data
    res = RES_Failed

    if verify_captcha(request) is not None:
        return verify_captcha(request)

    serializer = CustomUserSerializer(data=param)
    if serializer.is_valid():
        serializer.save()
        return Response(RES_SUCCESS, status=201)
    if 'username' in serializer.errors:
        res.update({'msg': '用户名已存在'})
    else:
        res.update({'msg': serializer.errors})
    return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    管理员登陆
    :param request: {'username':'string', password:'string'}
    :return: {'success':true|false, 'msg':'error',
            'data':{
                    'id': user.id,
                    'token': token,
                    'username': user.username,
                    'avatar': user.avatar,
                    'mobile': user.phone
                    }
                }
    """

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
def reset_password_view(request):
    """
    重置密码，用于已登录情况下
    :param request: {'old':'string', 'new':'string', 'captcha':'string'}
    :return: {'success':true|false, 'msg':'error'}
    """

    param = request.data
    res = RES_Failed

    if verify_captcha(request) is not None:
        return None

    try:
        user = User.objects.get(username=request.user.username)
        old_password = user.password
        if check_password(param['old'], old_password):
            user.set_password(param['new'])
            user.save()
            res = RES_SUCCESS
            return Response(res)
        res.update({'msg': '旧密码错误'})
        return Response(res)
    except Exception as e:
        res.update({'msg': str(e)})
        return Response(res)