from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('userlist', views.wip_userlist, name='wip_userlist'),
    path('paiement',views.paiement, name='paiement'),
    path('espacePerso',views.espacePerso, name='espacePerso'),
    path('inscription',views.inscription_user, name='inscription_user'),
    path('inscription_prod',views.inscription_prod, name='inscription_prod'),
    path('connexion', views.connexion, name='connexion'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('connexion', auth_views.LoginView.as_view()),
    path('personne/', views.delete_user, name='delete_user'),
    path('personne/<int:id>/', views.deleteOneUser, name='deleteOneUser'),
    path('listeCommande',views.listeCommande, name='listeCommande'),
    path('commande/<int:id>',views.commande, name='commande'),
    path('informationPerso',views.informationPerso, name='informationsPerso'),
    path('panier',views.panier, name='panier'),
    path('suppressionPanier/<int:id>',views.suppressionPanier, name='suppressionPanier'),

    
    
    #espace producteur 
    path('producteur/<int:idProducteur>', views.producteur, name='producteur'),
]