from django.urls import path

from . import views

urlpatterns = [
    path("login", views.quick_login_view, name="login"),
]
