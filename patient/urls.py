from django.urls import path

from . import views

urlpatterns = [
    path("list", views.list_view, name='list'),
    # path("update", views.update_view, name='update'),
]
