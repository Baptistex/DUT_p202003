from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views
from . import utils

urlpatterns = [
    path('userlist', views.wip_userlist, name='wip_userlist'),
    path('paiement',views.paiement, name='paiement'),
    path('espacePerso',views.espacePerso, name='espacePerso'),
    path('inscription',views.inscription_user, name='inscription_user'),
    path('inscription_prod',views.inscription_prod, name='inscription_prod'),
    path('connexion', views.connexion, name='connexion'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('connexion', auth_views.LoginView.as_view()),
    path('paiement', utils.send_mail_inscription, name='send_mail_inscription')

    
    
]