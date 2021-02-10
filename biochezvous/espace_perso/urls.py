from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('userlist', views.wip_userlist, name='wip_userlist'),
    path('paiement',views.paiement, name='paiement'),
    path('espacePerso',views.espacePerso, name='espacePerso'),
    path('inscription',views.inscription_prod, name='inscription_prod'),
    path('connexion', views.connexion_prod, name='connexion_prod'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    #path('Test',views.Test, name='Test'),

]