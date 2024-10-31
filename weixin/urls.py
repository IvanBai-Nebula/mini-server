from django.urls import path

from . import views

urlpatterns = [
    path("login", views.quick_login_view, name="login"),
    path("info", views.info_view, name="info"),
    path("list", views.list_view, name="list"),
    path("updata_avatar", views.updata_avatar_view, name="updata_avatar")
]
