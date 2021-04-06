from django.urls import path

from . import views

urlpatterns = [
    path('accueil', views.accueil, name='accueil'),
    path('', views.accueil, name='accueil2'),

    path('propos', views.propos, name='propos'),

]