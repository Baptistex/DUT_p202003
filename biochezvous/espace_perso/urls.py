from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    #Connexions/Inscriptions
    path('inscription',                     views.inscription_user,     name='inscription_user'),
    path('inscription/producteur',          views.inscription_prod,     name='inscription_prod'),
    path('connexion',                       views.connexion,            name='connexion'),
    path('connexion',                       auth_views.LoginView.as_view()),
    path('deconnexion',                     views.deconnexion,          name='deconnexion'),
    #Utilisateur        
    path('profil',                          views.espacePerso,          name='espacePerso'),
    path('profil/edit',                     views.informationPerso,     name='informationPerso'),
    path('profil/adresse/edit',             views.ajout_prod_adresse,   name='ajout_prod_adresse'),
    #Producteur
    path('profil/producteur/commandes',     views.commandeProducteur,   name='commandeProducteur'),
    #Panier/Commande
    path('profil/panier',                   views.panier,               name='panier'),
    path('profil/panier/<int:id>/suppression',views.suppressionPanier,  name='suppressionPanier'),
    path('profil/panier/commander',         views.commander,            name='commander'),
    path('profil/panier/paiement',          views.paiement,             name='paiement'),
    path('profil/commandes',                views.listeCommande,        name='listecommande'),
    path('profil/commande/<int:id>',        views.commande,             name='commande'),
    path('profil/panier/varier',            views.varierArticlePanier,  name='varierArticlePanier'),
    #Catalogue
    path('producteur/<int:idProducteur>',   views.producteur,           name='producteur'),
    #Administration
    path('personne/<int:id>/supprimer',     views.deleteOneUser,     name='deleteOneUser'),
    path('aide',                    views.aide,                 name='aide'),
    #Factures
    path('test',                    views.index,                name="test"),
    path('pdf_view/<int:id>',       views.PDF,                  name="pdf_view"),
    path('pdf_download/',           views.DownloadPDF.as_view(),name="pdf_download"),
    
]