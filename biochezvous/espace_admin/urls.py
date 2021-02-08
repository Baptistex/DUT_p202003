from django.urls import path
from . import views

urlpatterns = [
    path('accueilAdmin', views.espace_admin, name='espace_admin'),
    path('listeUtilisateurs', views.util_inscris, name='listeUtilisateurs')
]