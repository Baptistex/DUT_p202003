from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('paiement',views.paiement, name='paiement'),
    path('espacePerso',views.espacePerso, name='espacePersoUser'),
    path('inscription',views.inscription_user, name='inscription_user'),
    path('inscription_prod',views.inscription_prod, name='inscription_prod'),
    path('connexion', views.connexion, name='connexion'),
    path('deconnexion', views.deconnexion, name='deconnexion'),
    path('connexion', auth_views.LoginView.as_view()),
    path('aide', views.aide, name='aide'),
    path('personne/', views.delete_user, name='delete_user'),
    path('personne/<int:id>/', views.deleteOneUser, name='deleteOneUser'),
    path('accueilEspaceProducteur', views.espace_producteur, name='espace_producteur'),
    path('espaceProducteur',views.espacePersoProd, name='espacePersoProd'),
    path('listeCommande',views.listeCommande, name='listeCommande'),
    path('commande/<int:id>',views.commande, name='commande'),
    path('informationPerso',views.informationPerso, name='informationsPerso'),
    path('panier',views.panier, name='panier'),
    path('suppressionPanier/<int:id>',views.suppressionPanier, name='suppressionPanier'),
    path('decrementerArticlePanier/<int:id>',views.decrementerArticlePanier, name='decrementerArticlePanier'),
    path('incrementerArticlePanier/<int:id>',views.incrementerArticlePanier, name='incrementerArticlePanier'),
    path('nouvelleAdresse',views.ajout_prod_adresse, name='ajout_prod_adresse'),
    path('commander',views.commander, name='commander'),
    
    
    path('commandeProducteur',views.commandeProducteur, name='commandeProducteur'),

   
    #espace producteur 
    path('producteur/<int:idProducteur>', views.producteur, name='producteur'),
    path('test', views.index, name="test"),
    path('pdf_view/<int:id>', views.PDF, name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    
]