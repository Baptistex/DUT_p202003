from django.urls import path

from . import views

urlpatterns = [
    #Catalogue
    path('catalogue',                                   views.produit_django,               name='produit_django'),

    #Utilisateur
    path('produit/<int:idProduit>',                     views.produit,                      name='produit'),
    path('produit/preference/add/<int:produit>',        views.ajout_preference,             name='preference'),

    #Producteur
    path('categorie/ajouter',                           views.ajout_categorie,              name='ajout_categorie'),
    path('produits',                                    views.aff_prod,                     name='aff_prod'),    
    path('produit/ajouter',                             views.ajout_prod,                   name='ajout_prod'),
    path('produit/quantite',                            views.ajout_quantite,               name='ajout_quantite'),
    path('produit/images/priorite',                     views.update_image_priorite,        name='update_image_priorite'),
    path('produit/<int:id>/supprimer',                      views.deleteOneProd,            name='deleteOneProd'),
    path('producteur/produit/<int:id_produit>/images',  views.ajout_prod_image,             name='ajout_prod_image'),    
    path('producteur/produit/image/<int:id_image>/suppression',views.suppr_prod_image,      name='suppr_prod_image'),    

] 