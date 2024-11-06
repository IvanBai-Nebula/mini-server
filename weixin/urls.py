from django.urls import path

from . import views

urlpatterns = [
    path("quick_login", views.quick_login_view, name="quick_login"),
    path("info", views.info_view, name="info"),
    path("list", views.list_view, name="list"),
    path("update_avatar", views.update_avatar_view, name="update_avatar")
]
