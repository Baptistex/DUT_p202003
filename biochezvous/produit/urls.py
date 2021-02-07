from django.urls import path

from . import views

urlpatterns = [
    path('produits', views.liste_produit, name='liste_produit'),
    path('produit/<int:product_id>', views.produit, name='produit'),

    path('nouveauprod',views.ajout_prod, name='ajout_prod'),    
    path('produit',views.produit_django, name='produit_django'),

    path('ajoutquantite',views.ajout_quantite, name='ajout_quantite'),

    #Partie test lien entre pages django
    path('description',views.produit_description, name='produit_description'),


]