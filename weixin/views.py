import requests
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from utils.constants import *
from utils.permissions import IsWechatUser
from weixin.models import *
from weixin.serializer import CustomerUserSerializer, ProfileSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def quick_login_view(request):
    """
    微信用户快捷登录
    :param request: {'code': 'string'}
    :return: {'success': true | false, 'msg': 'error',
              'data': {
                    'token': token,
                    'username': user.username,
                    'avatar': user.avatar,
                    'phone': user.phone,
                }
            }
    """

    code = request.data['code']
    res = RES_Failed
    if not code:
        res.update({'msg': 'Missing code'})
        return Response(res)

    try:
        openid, session_key = get_openid(code)
    except Exception as e:
        res.update({'msg': str(e)})
        return Response(res)

    new = False

    try:
        user = CustomerUser.objects.get(id=openid)
    except CustomerUser.DoesNotExist:
        serializer = CustomerUserSerializer(data={'id': openid})
        if not serializer.is_valid():
            res.update({'msg': 'Serializer validation failed'})
            return Response(res)

        user = serializer.save(username=f"WX-{openid}")
        new = True

    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    res = RES_SUCCESS
    res.update({
        'data': {
            'username': user.username,
            'avatar': user.avatar,
            'phone': user.phone,
        },
        'token': token,
        'new': new
    })

    user.last_login = timezone.now()
    user.save()

    return Response(res)


def get_openid(code):
    """
    通过code获取openid
    :param code:
    :return: {'session_key': '', 'openid': ''} | error
    """

    app_id = APP_ID
    app_secret = APP_SECRET
    url = (f"https://api.weixin.qq.com/sns/jscode2session?"
           f"appid={app_id}&secret={app_secret}&js_code={code}&grant_type=authorization_code")

    response = requests.get(url)
    data = response.json()

    if 'errcode' in data and data['errcode'] != 0:
        raise Exception(data['errmsg'])

    openid = data.get('openid')
    session_key = data.get('session_key')

    if openid and session_key:
        return openid, session_key
    else:
        raise Exception("Failed to get openid and session_key: " + str(data))


@api_view(['GET'])
@permission_classes([AllowAny])
def info_view(request):
    """
    获取用户信息
    :param request:
    :return:
    {
    "success": true,
    "data": {
        "birthday": "string",
        "height": 0,
        "weight": 0,
        "pulse": 0,
        "blood_pressure": "string",
        "blood_sugar": 0,
        "blood_fat": 0
        }
    }
    """
    try:
        user = CustomerUser.objects.get(id=request.user.id)
    except CustomerUser.DoesNotExist:
        return Response({'msg': '没有此用户'})

    serializer = CustomerUserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_view(request):
    """
    获取用户列表
    :param request:
    :return:
    {
    "success": true,
    "data":
        {
        "id": 'openid',
        "username": "string",
        "avatar": "string",
        "phone": "string",
        "is_active": true
        }

     }
    """
    users = CustomerUser.objects.all()  # 获取所有用户
    user_data = []

    if users.exists():
        for user in users:
            user_data.append({
                'id': str(user.id),
                'username': user.username,
                'avatar': user.avatar if user.avatar else None,
                'phone': user.phone,
                'is_active': user.is_active,
            })
        return Response({
            'success': True,
            'data': user_data
        })
    else:
        return Response({
            'success': False,
            'error': "无用户."
        }, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_avatar_view(request):
    """
    更新用户头像
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

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def check_exist_view(request):
#     """
#     用于注册、更新个人信息时验证
#     :param request: {'value':'string', 'type':'username' }
#     :return: {'success':true | false, 'msg':'error'}
#     """
#
#     param = request.data
#     res = RES_Failed
#         if CustomerUser.objects.filter(username=param['value']).exists():
#             res.update({'msg': '用户名已存在'})
#             return Response(res)


# @api_view(['POST'])
# @permission_classes([AllowAny])
# def register(request):
#     """
#     用户注册
#     :param request: {'username': 'string', 'phone': 'string', 'code': 'string'}
#     :return:
#     {
#     "data": {
#         "username": "string",
#         "phone": "string",
#         "code": "string"
#         }
#     }
#     """
#     try:
#         user = CustomerUser.objects.get(username=request.data['username'])
#         return Response({'msg': '用户名已存在'})
#     except CustomerUser.DoesNotExist:
#         pass
#
#     try:
#         user = CustomerUser.objects.get(phone=request.data['phone'])
#         return Response({'msg': '手机号已存在'})
#     except CustomerUser.DoesNotExist:
#         pass
#
#     try:
#         code = Captcha.objects.get(phone=request.data['phone'], code=request.data['code'])
#     except Captcha.DoesNotExist:
#         return Response({'msg': '验证码错误'})
#
#     serializer = CustomerUserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.create(serializer.validated_data)
#         return Response({'msg': '注册成功'})
#     else:
#         return Response({'msg': '注册失败'})
