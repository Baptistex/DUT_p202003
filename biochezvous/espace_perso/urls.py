from django.urls import path

from . import views

urlpatterns = [
    path('', views.wip_userlist, name='wip_userlist'),
    path('',views.wip_connexion, name='wip_connexion'),
    path('',views.wip_inscription, name='wip_inscription'),
]