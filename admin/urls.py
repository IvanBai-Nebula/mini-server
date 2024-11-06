from django.urls import path

from . import views

urlpatterns = [
    path('register', views.register_view, name='register'),
    path('login', views.login_view, name='login'),
    path('reset_password', views.reset_password_view, name='reset_password'),
    path('check_exist', views.check_exist_view, name='check_exist'),
    path('send_email_captcha', views.send_email_captcha_view, name='send_email_captcha'),
    path('list', views.list_view, name='list'),
    path('updata_avatar', views.update_avatar_view, name='update_avatar')

]
