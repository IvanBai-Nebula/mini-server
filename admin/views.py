import random
import string
from datetime import timedelta

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.utils import timezone
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
    :return: {'success':true | false, 'msg':'error'}
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

        照护日记团队
        """

        send_mail("照护者后台注册验证码", message=message,
                  recipient_list=[email], from_email=None)

        # TODO: 后期用缓存实现存储验证码，这里目前使用session

        request.session['captcha'] = captcha
        request.session.set_expiry(timedelta(minutes=10).total_seconds())

        return Response(RES_SUCCESS)
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
    :return: {'success':true | false, 'msg':'error'}
    """

    param = request.data
    res = RES_Failed

    if verify_captcha(request) is not None:
        return verify_captcha(request)

    serializer = UserSerializer(data=param)
    if serializer.is_valid():
        serializer.save()
        return Response(RES_SUCCESS)
    if 'username' in serializer.errors:
        res.update({'msg': '用户名已存在'})
    else:
        res.update({'msg': serializer.errors})
    return Response(res)


@api_view(['POST'])
@permission_classes([AllowAny])
def check_exist_view(request):
    """
    用于注册、更新个人信息时验证
    :param request: {'value':'string', 'type':'username' | 'email' | 'phone'}
    :return: {'success':true | false, 'msg':'error'}
    """

    param = request.data
    res = RES_Failed
    match param['type']:
        case 'username':
            if User.objects.filter(username=param['value']).exists():
                res.update({'msg': '用户名已存在'})
                return Response(res)
        case 'email':
            if User.objects.filter(email=param['value']).exists():
                res.update({'msg': '邮箱已存在'})
                return Response(res)
        case 'phone':
            if User.objects.filter(phone=param['value']).exists():
                res.update({'msg': '手机号已存在'})
                return Response(res)
        case _:
            res.update({'msg': '参数错误'})
            return Response(res)

    return Response(RES_SUCCESS)


def login_success(user):
    res = RES_SUCCESS
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    user.private_key = private_key

    res.update({
        'data': {
            'id': user.id,
            'username': user.username,
            'avatar': user.avatar,
            'phone': user.phone,
            'email': user.email
        },
        'token': token,
        'public_key': public_key
    })
    user.last_login = timezone.now()
    user.save()
    return Response(res)


def decrypt_data(encrypted_data, private_key):
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    管理员登陆
    :param request: {'username':'string', password:'string'}
    :return: {'success':true | false, 'msg':'error',
            'data':{
                    'id': user.id,
                    'username': user.username,
                    'avatar': user.avatar,
                    'phone': user.phone,
                    'email': user.email
                    }
            'token': token,
                }
    """

    res = RES_Failed
    username = request.data['username']
    raw_password = request.data['password']

    if not username or not raw_password:
        res.update({'msg': '用户名或密码不能为空'})
        return Response(res)

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        res.update({'msg': '用户不存在'})
        return Response(res)

    # 使用 Django 内置方法验证用户
    private_key = user.private_key
    password = decrypt_data(raw_password, private_key)
    user = authenticate(username=username, password=password)

    if user is None:
        res.update({'msg': '用户名或密码错误'})
        return Response(res, status=401)

    return login_success(user)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def reset_password_view(request):
    """
    重置密码，用于已登录情况下
    :param request: {'old':'string', 'new':'string', 'captcha':'string'}
    :return: {'success':true | false, 'msg':'error'}
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
            return Response(RES_SUCCESS)

        res.update({'msg': '旧密码错误'})
        return Response(res)
    except Exception as e:
        res.update({'msg': str(e)})
        return Response(res)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def list_view(request):
    """
    列出所有用户
    :param request:
    :return:{"success": true
        'data':{'id':'uuid',
                'username':'string',
                'avatar':'string',
                'is_staff': true,
                'is_active': true
         }
       }
    """
    users = User.objects.all()  # 获取所有用户
    user_data = []

    if users.exists():  # 检查是否存在用户
        for user in users:
            user_data.append({
                'data': {
                    'id': str(user.id),
                    'username': user.username,
                    'avatar': user.avatar.url if user.avatar else None,
                    'is_staff': user.is_staff,
                    'is_active': user.is_active,
                }
            })
        return Response({
            'success': True,
            'data': user_data
        })
    else:
        return Response({
            'success': False,
            'error': '没有用户数据可返回'
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_avatar_view(request):
    """
    更新管理员头像
    :param request: {'avatar': 'string'}
    :return:
    {
    "success": true
    """
    user = request.user  # 获取当前用户

    if 'avatar' not in request.FILES:
        return Response({'msg': '缺少头像文件'})

    user.avatar = request.FILES['avatar']
    user.save()

    return Response({'msg': '头像更新成功', 'avatar': user.avatar.url})