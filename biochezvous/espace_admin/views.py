from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from espace_perso.models import Personne, Utilisateur, Producteur
from produit.models import Commande
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Demandes
from .forms import FormAideReponse

#Accueil
def espace_admin(request):
    template = loader.get_template('espace_admin/accueil_admin.html')
    nbPers = Personne.objects.all();
    nbComm = Commande.objects.all();
    return HttpResponse(template.render({'nbPers':nbPers,'nbComm':nbComm},request))

#Liste de tous les utilisateurs
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

#Liste des clients
def clientlist(request):

    template = loader.get_template('espace_admin/devenir_prod.html')
    id = str(Personne.personne_id)
    table_client = Personne.objects.exclude(personne_id__in = Producteur.objects.all())

    context = {
        'clientlist': table_client
    }

    return HttpResponse(template.render(context,request))

#Faire passer un client en producteur
def devenirPro(request,id):

    if request.method == "GET":

        client = Personne.objects.get(personne_id = id)
        newProd = Producteur(client)
        newProd.__dict__.update(client.__dict__)
        newProd.save()
        
        message = render_to_string('confirmation_prod.html', {
            'user': client,
            })
        send_mail(
            'Bienvenu !',
            message,
            'sav.biochezvous@gmail.com',
            (client.mail,),
            fail_silently=False, 
            auth_user=None, 
            auth_password=None, 
            connection=None, 
            html_message=None
        )

        template = loader.get_template('espace_admin/devenir_prod.html')
        table_client = Personne.objects.exclude(personne_id__in = Producteur.objects.all())

        context = {
            'clientlist': table_client
        }

    return HttpResponse(template.render(context,request))

#Afficher la liste des demandes d'aide et envoie d'un mail de réponse via le formulaire
def util_aide(request):

    template = loader.get_template('espace_admin/aide.html')
    table_demandes = Demandes.objects.all()

    if request.method == "POST":
        form = FormAideReponse(request.POST)
        if form.is_valid():

            objet = form.cleaned_data['objet']
            message = form.cleaned_data['message']
            destinataire = form.cleaned_data['destinataire']

            send_mail(
                objet,
                message,
                'sav.biochezvous@gmail.com',
                (destinataire,),
                fail_silently=False, 
                auth_user=None, 
                auth_password=None, 
                connection=None, 
                html_message=None
            )

        return redirect('/listeAides')
    else:
        form = FormAideReponse()

    context = {
        'listeAides' : table_demandes,
        'form' : form
    }
    return HttpResponse(template.render(context,request))


#Supprimer un message de demande  
def deleteDemande(request,msg_id):

    if request.method == "GET":
        delDemande = Demandes.objects.get(message_id = msg_id) # On récupère l'id attribué au message
        delDemande.delete()

        template = loader.get_template('espace_admin/aide.html') # Retour à la liste une fois la suppression faite
        table_demandes = Demandes.objects.all()

        context = {
            'listeAides' : table_demandes
        }

    return HttpResponse(template.render(context,request))
