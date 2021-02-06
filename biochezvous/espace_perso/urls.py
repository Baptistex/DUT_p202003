from django.urls import path
from .forms import ProducteurFormConnexion
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('userlist', views.wip_userlist, name='wip_userlist'),
    path('connexion', views.wip_connexion, name='wip_connexion'),
    path('inscription',views.wip_inscription, name='wip_inscription'),
    path('paiement',views.paiement, name='paiement'),
    path('inscription_prod',views.inscription_prod, name='inscription_prod'),
    path('connexion_prod', views.connexion_prod, name='connexion_prod'),


]