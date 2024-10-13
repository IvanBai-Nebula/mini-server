from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """
    自定义权限类：仅允许管理员用户访问
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsWechatUser(BasePermission):
    """
    自定义权限类：仅允许微信用户访问
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and not request.user.is_staff)
