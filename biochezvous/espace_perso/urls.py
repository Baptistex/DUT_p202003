from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from . import views
from . import utils

urlpatterns = [
    #Connexions/Inscriptions
    path('inscription',                     views.inscription_user,     name='inscription_user'),
    path('inscription/producteur',          views.inscription_prod,     name='inscription_prod'),
    path('connexion',                       views.connexion,            name='connexion'),
    path('connexion',                       auth_views.LoginView.as_view()),
    path('deconnexion',                     views.deconnexion,          name='deconnexion'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    #Utilisateur        
    path('profil',                          views.espacePerso,          name='espacePerso'),
    path('profil/edit',                     views.informationPerso,     name='informationPerso'),
    path('profil/adresse/edit',             views.ajout_prod_adresse,   name='ajout_prod_adresse'),
    path('profil/mesPreferences',             views.preferences,   name='mesPreferences'),
    #Producteur
    path('profil/producteur/commandes',     views.commandeProducteur,   name='commandeProducteur'),
    path('producteur/terminerCommander/<int:commande_id>',views.terminerCommande,name='terminerCommande'),
    #Panier/Commande
    path('profil/panier',                   views.panier,               name='panier'),
    path('profil/panier/<int:id>/suppression',views.suppressionPanier,  name='suppressionPanier'),
    path('profil/panier/commander',         views.commander,            name='commander'),
    path('profil/panier/paiement',          views.paiement,             name='paiement'),
    path('profil/commandes',                views.listeCommande,        name='listecommande'),
    path('profil/commande/<int:id>',        views.commande,             name='commande'),
    path('profil/panier/varier',            views.varierArticlePanier,  name='varierArticlePanier'),
    path('send_mail_commande/<int:commande_id>',views.send_mail_commande,name='send_mail_commande'),
    path('profil/commanderEncore/<int:id>',        views.commanderEncore,             name='commanderEncore'),
    #Catalogue
    path('producteur/<int:idProducteur>',   views.producteur,           name='producteur'),
    #Administration
    path('personne/<int:id>/supprimer',     views.deleteOneUser,     name='deleteOneUser'),
    path('aide',                    views.aide,                 name='aide'),
    #Factures
    path('pdf_view/<int:id>',       views.PDF,                  name="pdf_view"),
    
]