from django.urls import path

from . import views

urlpatterns = [
    path('produits', views.liste_produit, name='liste_produit'),
    path('produit/<int:product_id>', views.produit, name='produit'),
    path('nouveauprod',views.ajout_prod, name='ajout_prod'),
]