from django.urls import path

from . import views

urlpatterns = [
    path('', views.wip_userlist, name='wip_userlist'),
]