from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.template import loader
from espace_perso.models import Personne, Utilisateur, Producteur
from .forms import ContactFormInscription


# Create your views here.


def wip_userlist(request):

    template = loader.get_template('espace_perso/wip_userlist.html')
    #Creation de manière statique d'une personne (exemple)
    pers = Utilisateur(nom = "paul", prenom = "patate", mot_de_passe = "aaa", mail = "a@a.fr", num_tel = "01")
    #Sauvegarde de la personne dans la bdd
    pers.save()

    #Recuperation de toute la table personne dans une variable table_pers
    #  et passage a la template via context
    table_pers = Utilisateur.objects.all()
    context = {
        'userlist': table_pers
    }
    return HttpResponse(template.render(context,request))


def wip_connexion(request):
    template = loader.get_template('espace_perso/wip_connexion.html')
    return HttpResponse(template.render({},request))

def wip_inscription(request):
    template = loader.get_template('espace_perso/wip_inscription.html')
    return HttpResponse(template.render({},request))

def paiement(request):
    template = loader.get_template('espace_perso/paiement.html')
    return HttpResponse(template.render({},request))

