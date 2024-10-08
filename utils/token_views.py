from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@api_view(['POST'])
def custom_token_obtain_pair(request):
    serializer = TokenObtainPairView.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
        tokens = serializer.validated_data
        return Response({
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh']
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def custom_token_refresh(request):
    serializer = TokenRefreshView.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
        tokens = serializer.validated_data
        return Response({
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh']
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
