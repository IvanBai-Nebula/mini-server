from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('reset_password/', views.reset_password_view, name='reset_password'),
    path('send_email_captcha/', views.send_email_captcha_view, name='send_email_captcha')

]
