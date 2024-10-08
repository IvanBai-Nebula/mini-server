import requests
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.permissions import IsAdminUser
from .models import *
from .serializer import *

APP_ID = 'wx1234567890abcdef'
APP_SECRET = '1234567890abcdef1234567890abcdef'

REQUEST_SOURCE_WEB = 'web'
REQUEST_SOURCE_MINIAPP = 'miniapp'

RES_SUCCESS = {'success': True}
RES_Failed = {'success': False}


@api_view(['POST'])
def register_view(request):
    data = request.data
    res = RES_SUCCESS
    serializer = CustomUserSerializer(data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(res, status=201)
    res = RES_Failed.update({'msg': serializer.errors})
    return Response(res)


@api_view(['POST'])
def login_view(request):
    request_source = request.headers.get('Request-Source')
    params = request.data
    print(params)
    res = {'success': True}
    if request_source == REQUEST_SOURCE_WEB:
        return handle_web_login(params, res)
    elif request_source == REQUEST_SOURCE_MINIAPP:
        return handle_miniapp_login(params, res)
    return Response({'success': False, 'msg': '请求来源错误'})


def handle_web_login(params, res):
    username = params.get('username')
    password = params.get('password')

    try:
        user = User.objects.get(username=username)
        # check_password(password, user.password)
        token = generate_token(user)
        res.update({'data': {'token': token, 'username': user.username,
                             'avatar': user.avatar}})
    except Exception as e:
        return Response({'success': False, 'msg': str(e)})


def handle_miniapp_login(request):
    code = request.POST.get('code')
    if not code:
        return Response({'success': False, 'msg': 'code不能为空', 'data': {}})

    try:
        url = ('https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={'
               '}&grant_type=authorization_code').format(APP_ID, APP_SECRET, code)
        response = requests.get(url)
        data = response.json()

        openid = data.get('openid')
        if openid:
            user, created = User.objects.get_or_create(openid=openid, defaults={'username': openid, 'role': 2})
            token = generate_token(user)
            msg = '新用户注册成功' if created else '登录成功'
            return Response({'success': True, 'msg': msg, 'data': {'token': token, 'username': user.username,
                                                                   'avatar': user.avatar}})
        else:
            return Response({'success': False, 'msg': '获取openid失败', 'data': {}})
    except requests.exceptions.RequestException:
        return Response({'success': False, 'msg': '微信服务器请求失败', 'data': {}})
    except Exception as e:
        return Response({'success': False, 'msg': str(e), 'data': {}})

# def generate_token(user):
#     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#     payload = jwt_payload_handler(user)
#     return jwt_encode_handler(payload)
