from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Info, CustomerUser
from weixin.serializer import CustomerUserSerializer
from patient.models import Info
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializer import InfoSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def list_view(request):
    try:
        # 获取当前用户
        user = CustomerUser.objects.get(id=request.user.id)
    except CustomerUser.DoesNotExist:
        return Response({'msg': '没有此用户'})

    # 获取与当前用户关联的病人
    patients = user.patients.all()

    # 序列化病人数据
    serializer = InfoSerializer(patients, many=True)

    # 返回病人数据
    return Response(serializer.data)

# @api_view(['PUT'])
# @permission_classes([AllowAny])
# def update_view(request):
#     try:
#         # 获取用户
#         user = CustomerUser.objects.get(id=request.user.id)
#     except CustomerUser.DoesNotExist:
#         return Response({'msg': '没有此用户'})
#
#     # 如果请求体中包含病人信息
#     if 'patients' in request.data:
#         # 处理病人的数据
#         patients_data = request.data['patients']
#
#         # 确保是一个列表（即添加多个病人）
#         if not isinstance(patients_data, list):
#             return Response({"detail": "Patients should be a list."}, status=status.HTTP_400_BAD_REQUEST)
#
#         # 将传入的病人数据序列化并创建/更新病人实例
#         for patient_data in patients_data:
#             # 创建病人或查找已有的病人
#             patient_serializer = InfoSerializer(data=patient_data)
#             if patient_serializer.is_valid():
#                 patient = patient_serializer.save()
#                 # 将病人与用户关联
#                 user.patients.add(patient)
#             else:
#                 return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     # 返回更新后的用户数据
#     user_serializer = CustomerUserSerializer(user)
#     return Response(user_serializer.data, status=status.HTTP_200_OK)
