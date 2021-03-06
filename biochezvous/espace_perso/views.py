from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from .models import Utilisateur,Personne
from espace_perso.forms import FormInscriptionProd
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from .forms import FormInscription, FormConnexion, FormDataModification, FormInscriptionUser #, Suppression


# Create your views here.

def wip_userlist(request):
    template = loader.get_template('espace_perso/wip_userlist.html')
    table_pers = Personne.objects.all()
    context = {
        'userlist': table_pers
    }

    return HttpResponse(template.render(context,request))

def delete_user(request):
    if request.method == "GET":
        dest = Personne.objects.all()
        dest.delete()
        template = loader.get_template('espace_perso/wip_userlist.html')
        table_pers = Personne.objects.all()
        context = {
            'userlist': table_pers
        }
    return HttpResponse(template.render(context,request))
    
def deleteOneUser(request,id):
    if request.method == "GET":
        dest = Personne.objects.get(personne_id = id)
        dest.delete()
        template = loader.get_template('espace_perso/wip_userlist.html')
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

    
def inscription_user(request):
    if request.method == 'POST':
        form = FormInscriptionUser(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/connexion')
    else:
        form = FormInscriptionUser()
    #TODO : un template propre à chaque type d'inscription
    return render(request, 'espace_perso/inscription_prod.html', {'form' : form})

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

def connexion(request):
    verif_connexion = "Vous n'êtes pas connecté."
    if request.user.is_authenticated:
        verif_connexion = "Vous êtes connecté."
    #Affiche tous les proucteurs
    print(Personne.objects.filter(groups__name='producteur'))
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


#def modifDataUtilisateur(request):
#def espacePerso(request):
@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def espacePerso(request):
    #TODO changer et unifier le bazar
    #TODO voir les sessions pour récupérer l'id
    #TODO Vérifier les champs
    personne_id = request.user.personne_id
    u = Personne.objects.get(personne_id=personne_id)
    form = FormDataModification(instance=u)
    if request.method == 'POST' :
        form = FormDataModification(request.POST, instance=u)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'espace_perso/espacePerso.html', context)

#   Utilisez ces fonctions (en remplaçant name et codename) pour ajouter une permission à un groupe
#def update_Permissions(request):
#    prod_group, created = Group.objects.get_or_create(name='producteur')
#    print(prod_group.permissions)
#    prod_group.permissions.add(
#        Permission.objects.get(codename='can_view_espace_perso')
#    )
    
