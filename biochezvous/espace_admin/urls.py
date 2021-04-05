from django.urls import path,include
from . import views
import produit.views

urlpatterns = [
    path('accueilAdmin', views.espace_admin, name='espace_admin'),
    path('userlist', views.userlist, name='userlist'),
    path('clientlist', views.clientlist, name='clientlist'),
    path('personne/<int:id>', views.devenirPro, name='devenirPro'),
    path('listeAides', views.util_aide, name='listeAides'),
    path('personne/', views.delete_user, name='delete_user'),
    path('personne/<int:id>/', views.deleteOneUser, name='deleteOneUser'),
    path('demande/<int:msg_id>/', views.deleteDemande, name='deleteDemande'),
    path('nouveautype',produit.views.addType, name='ajout_type'),
]