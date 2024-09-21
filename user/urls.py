from django.urls import path

from .views import *

urlpatterns = [
    path("test/list", TestView.as_view(), name="list"),
    path("test/jwt", JwtTestView.as_view(), name="jwt"),
    path("admin/login", AdminLoginView.as_view(), name="admin_login"),
    # path("admin/user_info_list"),
    path("mini/user_info", UserInfoView.as_view(), name="user_info")
]
