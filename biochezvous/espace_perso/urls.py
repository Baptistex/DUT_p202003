from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('userlist', views.wip_userlist, name='wip_userlist'),
    path('connexion', views.wip_connexion, name='wip_connexion'),
    path('inscription',views.wip_inscription, name='wip_inscription'),
    path('paiement',views.paiement, name='paiement'),
    path('espacePerso',views.espacePerso, name='espacePerso'),

    path('inscription_prod',views.inscription_prod, name='inscription_prod'),
    path('connexion_prod', views.connexion_prod, name='connexion_prod'),
    path('deconnexion', views.deconnexion, name='deconnexion'),


]