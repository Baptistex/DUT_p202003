from django.shortcuts import render
from django.http import HttpResponse
from django.db import connection
from collections import namedtuple
from django.template import loader
from espace_perso.models import Personne


# Create your views here.


def wip_userlist(request):

    template = loader.get_template('espace_perso/wip_userlist.html')
    #Creation de manière statique d'une personne (exemple)
    pers = Personne(nom = "michel", prenom = "patate", mot_de_passe = "aaa", mail = "a@a.fr", num_tel = "01")
    #Sauvegarde de la personne dans la bdd
    pers.save()

    #Recuperation de toute la table personne dans une variable table_pers
    #  et passage a la template via context
    table_pers = Personne.objects.all()
    context = {
        'userlist': table_pers
    }
    

    return HttpResponse(template.render(context,request))