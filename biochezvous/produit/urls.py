from django.urls import path

from . import views

urlpatterns = [
    
    path('produit/<int:idProduit>', views.produit, name='produit'),

    path('nouveauprod',views.ajout_prod, name='ajout_prod'),
    path('afficherproduit',views.aff_prod, name='aff_prod'),    
    path('nouvelleimage',views.ajout_prod_image, name='ajout_prod_image'),    

    path('produits',views.produit_django, name='produit_django'),

    path('ajoutquantite',views.ajout_quantite, name='ajout_quantite'),

    #Partie test lien entre pages django
    path('description',views.produit, name='produit_description'),
    path('nouvellecategorie',views.ajout_categorie, name='ajout_categorie'),
    

    path('produit/<int:id>/', views.deleteOneProd, name='deleteOneProd'),
] 