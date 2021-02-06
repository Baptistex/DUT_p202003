from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader

from .models import Personne, Utilisateur, Producteur
from .forms import ContactFormInscription, ProducteurFormConnexion, ProducteurFormInscription


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
    if request.method == 'POST':
        form = ContactFormInscription(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/')
    else:
        form = ContactFormInscription()
    return render(request, 'espace_perso/wip_inscription.html', {'form': form})


def paiement(request):
    template = loader.get_template('espace_perso/paiement.html')
    return HttpResponse(template.render({},request))

def inscription_prod(request):
    template = loader.get_template('espace_perso/inscription_prod.html')
    return HttpResponse(template.render({},request))

def connexion_prod(request):
    if request.method == 'POST':
        form = ProducteurFormConnexion(request.POST, request.FILES)
        if form.is_valid():
            
            #TODO: changer la redirection
            return HttpResponseRedirect('/')
    else:
        form = ProducteurFormConnexion()
    return render(request, 'espace_perso/connexion_prod.html', {'form' : form})

