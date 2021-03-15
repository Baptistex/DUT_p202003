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
from produit.models import Commande, ContenuCommande, Panier, Produit


# Create your views here.

def wip_userlist(request):
    template = loader.get_template('espace_perso/wip_userlist.html')
    #if  person_id == None:
    #person = Personne()
    #else:
    #person = Personne.objects.get(personne_id = 10)
    table_pers = Personne.objects.all()
    context = {
        'userlist': table_pers
    }
    #Suppression
    #person.delete();
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
        form = FormInscriptionProd()
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


@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def espacePerso(request):
    """
    Vue qui permet d'accéder aux fonctionnalités concernant l'espace perso

    Args:

    Returns:
        contenuCommande : liste des produits contenu dans la commande
        Commande : les infos concernant la commande

    Authors:
        Justine Fouillé
    """
    context = {}
    return render(request, 'espace_perso/espacePerso.html', context)



#   Utilisez ces fonctions (en remplaçant name et codename) pour ajouter une permission à un groupe
#def update_Permissions(request):
#    prod_group, created = Group.objects.get_or_create(name='producteur')
#    print(prod_group.permissions)
#    prod_group.permissions.add(
#        Permission.objects.get(codename='can_view_espace_perso')
#    )
    
@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def listeCommande(request):
    """
    Afficher les différentes commandes d'un utilisateur

    Args:

    Returns:
        commandes : listes des commandes de l'utilisateur

    Authors:
        Justine Fouillé
    """
    context = {}
    personne_id = request.user.personne_id
    context['commandes'] = Commande.objects.filter(personne_id=personne_id)    
    return render(request, 'espace_perso/listeCommande.html',context)

#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def commande(request,id):
    """
    Afficher les produits d'une commande donnée

    Args:
        id : numéro de la commande dont on veut le détail

    Returns:
        contenuCommande : liste des produits contenu dans la commande
        Commande : les infos concernant la commande

    Authors:
        Justine Fouillé
    """
    context = {}
    context['contenuCommande'] = ContenuCommande.objects.filter(commande_id=id)
    context['Commande'] = Commande.objects.get(commande_id=id)
    
    return render(request, 'espace_perso/commande.html',context)


@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def informationPerso(request):
    """
    Afficher les infos persos de l'utilisateur afin qu'il puisse les modifier

    Args:

    Returns:
        form : formulaire avec les informations prérentrer dedans

    Authors:
        Justine Fouillé
    """
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


    return render(request, 'espace_perso/informationPerso.html', context)


#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def panier(request):
    """
    Afficher le panier : les articles que l'utilisateur souhaite acheter mais qui ne sont pas encore commandes

    Args:

    Returns:
        panier : le panier de l'utilisateur

    Authors:
        Justine Fouillé
    """
    context = {}
    personne_id = request.user.personne_id
    context['panier'] = Panier.objects.filter(personne_id=personne_id)    
    return render(request, 'espace_perso/panier.html',context)

def suppressionPanier(request):
    context = {}
    return render(request, 'espace_perso/suppressionPanier.html',context)