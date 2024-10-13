import requests
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from utils.constants import *
from weixin.models import *
from weixin.serializer import CustomerUserSerializer


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
            'token': token,
            'username': user.username,
            'avatar': user.avatar,
            'phone': user.phone,
        },
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
