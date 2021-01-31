from django.urls import path

from . import views

urlpatterns = [
    path('userlist', views.wip_userlist, name='wip_userlist'),
    path('connexion', views.wip_connexion, name='wip_connexion'),
    path('inscription',views.wip_inscription, name='wip_inscription'),
    path('paiement',views.paiement, name='paiement'),


]