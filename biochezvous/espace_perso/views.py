from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .models import Utilisateur,Personne
from .forms import FormInscription, FormConnexion, TestForm
from espace_perso.forms import FormInscriptionProd
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission


# Create your views here.


def wip_userlist(request):
#Suppression
#b = Blog.objects.get(pk=1)
# This will delete the Blog and all of its Entry objects.
#b.delete()

    template = loader.get_template('espace_perso/wip_userlist.html')
    #Recuperation de toute la table personne dans une variable table_pers
    #  et passage a la template via context
    table_pers = Personne.objects.all()
    context = {
        'userlist': table_pers
    }
    return HttpResponse(template.render(context,request))


def wip_connexion(request):
    template = loader.get_template('espace_perso/wip_connexion.html')
    return HttpResponse(template.render({},request))

def wip_inscription(request):
    if request.method == 'POST':
        form = FormInscription(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/connexion')
    else:
        form = FormInscription()
    return render(request, 'espace_perso/wip_inscription.html', {'form': form})

@permission_required ('espace_perso.can_view_espace_perso')
def paiement(request):
    template = loader.get_template('espace_perso/paiement.html')
    return HttpResponse(template.render({},request))

def espacePerso(request):
    template = loader.get_template('espace_perso/espacePerso.html')
    return HttpResponse(template.render({},request))

def inscription_prod(request):
    if request.method == 'POST':
        form = FormInscriptionProd(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/connexion')
    else:
        form = FormInscriptionProd()
    return render(request, 'espace_perso/inscription_prod.html', {'form' : form})

def connexion_prod(request):
    verif_connexion = "Vous n'êtes pas connecté."
    if request.user.is_authenticated:
        verif_connexion = "Vous êtes connecté."

    if request.method == 'POST':
        form = FormConnexion(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return HttpResponseRedirect('/')

    else:
        form = FormConnexion()
    return render(request, 'espace_perso/connexion_prod.html', {'form' : form, 'verif_connexion' : verif_connexion})


def deconnexion(request):
    template = loader.get_template('espace_perso/deconnexion.html')
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse(template.render({},request))

"""
def modif_data(request):

    if request.method == 'POST':
        form = FormDataModification(request.POST)

        #email = request.POST.get('email')
        #name = request.POST.get('name')

        instance = form.save()
        instance.save() 
    else:
        #form = FormInscription()
    return render(request, 'espace_perso/inscription_prod.html', {'form' : form})
"""


def Test(request):
    form = TestForm()
    context = {'form':form}
    return render(request, 'espace_perso/inscription_prod.html', {'form' : form})

#   Utilisez ces fonctions (en remplaçant name et codename) pour ajouter une permission à un groupe
#def update_Permissions(request):
#    prod_group, created = Group.objects.get_or_create(name='producteur')
#    print(prod_group.permissions)
#    prod_group.permissions.add(
#        Permission.objects.get(codename='can_view_espace_perso')
#    )