from django.urls import path
from . import views

urlpatterns = [
    path('accueilAdmin', views.espace_admin, name='espace_admin'),
    path('userlist', views.userlist, name='userlist'),
    path('listeAides', views.util_aide, name='listeAides'),

]