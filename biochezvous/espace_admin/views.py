from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from espace_perso.models import Personne
from espace_perso.forms import FormAide
from .models import Demandes #importer modèle de 'espace_perso' - pas nécessaire de recréer modèle personne

#Accueil
def espace_admin(request):
    template = loader.get_template('espace_admin/accueil_admin.html')
    return HttpResponse(template.render({},request))

#Liste utilisateurs
def userlist(request):
    template = loader.get_template('espace_admin/userlist.html')
    table_pers = Personne.objects.all()
    context = {
        'userlist': table_pers
    }

    return HttpResponse(template.render(context,request))

#Supprimer tous les utilisateurs
def delete_user(request):

    if request.method == "GET":

        dest = Personne.objects.all()
        dest.delete()

        template = loader.get_template('espace_admin/userlist.html')
        table_pers = Personne.objects.all()

        context = {
            'userlist': table_pers
        }

    return HttpResponse(template.render(context,request))

#Supprimer un utilisateur choisi 
def deleteOneUser(request,id):

    if request.method == "GET":

        dest = Personne.objects.get(personne_id = id)
        dest.delete()
        
        template = loader.get_template('espace_admin/userlist.html')
        table_pers = Personne.objects.all()

        context = {
            'userlist': table_pers
        }

    return HttpResponse(template.render(context,request))

#Afficher la liste des demandes d'aide
def util_aide(request):
    template = loader.get_template('espace_admin/aide.html')
    table_demandes = Demandes.objects.all()
    context = {
        'listeAides' : table_demandes
    }
    return HttpResponse(template.render(context,request))

#Supprimer un message de demande  
def deleteDemande(request,msg_id):

    if request.method == "GET":
        delDemande = Demandes.objects.get(message_id = msg_id) #On récupère l'id attribué au message
        delDemande.delete()

        template = loader.get_template('espace_admin/aide.html') #Retour à la liste une fois la suppression faite
        table_demandes = Demandes.objects.all()

        context = {
            'listeAides' : table_demandes
        }

    return HttpResponse(template.render(context,request))
