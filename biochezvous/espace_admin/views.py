from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from espace_perso.models import Personne, Utilisateur, Producteur
from espace_perso.forms import FormConnexion
from produit.models import Commande, ContenuCommande
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Demandes
from .forms import FormAideReponse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.utils.html import strip_tags
from django.contrib.auth.decorators import permission_required
from django.contrib.auth import authenticate, login, logout



#Accueil
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
def espace_admin(request):
    template = loader.get_template('espace_admin/accueil_admin.html')
    nbPers = Personne.objects.all();
    nbComm = Commande.objects.all();
    return HttpResponse(template.render({'nbPers':nbPers,'nbComm':nbComm},request))

#Liste de tous les utilisateurs
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
def userlist(request):
    template = loader.get_template('espace_admin/userlist.html')
    table_pers = Personne.objects.all()
    context = {
        'userlist': table_pers
    }

    return HttpResponse(template.render(context,request))

#Supprimer tous les utilisateurs
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
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
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
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
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
def clientlist(request):

    template = loader.get_template('espace_admin/devenir_prod.html')
    id = str(Personne.personne_id)
    table_client = Personne.objects.exclude(personne_id__in = Producteur.objects.all())

    context = {
        'clientlist': table_client
    }

    return HttpResponse(template.render(context,request))

#Faire passer un client en producteur
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
def devenirPro(request,id):
    if request.method == "GET":

        client = Personne.objects.get(personne_id = id)
        newProd = Producteur(client)
        newProd.__dict__.update(client.__dict__)
        newProd.save()
        mail_subject = 'Bienvenue !'
        message = render_to_string('confirmation_prod.html', {
            'user': client,
            'title': 'Confirmation producteur',
            })
        text_content = strip_tags(message)
        email = EmailMultiAlternatives(
            mail_subject, message, to=[client.mail]
        )
        email.attach_alternative(message, "text/html")
        email.send()

        template = loader.get_template('espace_admin/devenir_prod.html')
        table_client = Personne.objects.exclude(personne_id__in = Producteur.objects.all())

        context = {
            'clientlist': table_client
        }

    return HttpResponse(template.render(context,request))

#Afficher la liste des demandes d'aide et envoie d'un mail de réponse via le formulaire
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
def util_aide(request):
    template = loader.get_template('espace_admin/aide.html')
    table_demandes = Demandes.objects.all()

    if request.method == "POST":
        form = FormAideReponse(request.POST)
        if form.is_valid():
            
            objet = form.cleaned_data['objet']
            message = form.cleaned_data['message']
            destinataire = form.cleaned_data['destinataire']

            html_content = render_to_string("aide_reponse.html", {'title':'réponse mail','content':message})
            text_content = strip_tags(html_content)


            email = EmailMultiAlternatives(
                        objet, message, to=[destinataire]
            )
            email.attach_alternative(html_content, "text/html")
            email.send()

        return redirect('listeAides')
    else:
        form = FormAideReponse()

    context = {
        'listeAides' : table_demandes,
        'form' : form
    }
    return HttpResponse(template.render(context,request))


#Supprimer un message de demande  
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
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

#Liste de toutes les commandes et afficher le détail de chaque commande
@permission_required ('espace_perso.can_view_espace_admin', login_url='connexion')
def listeCommande(request):

    context = {}
    context['commandes'] = Commande.objects.all()   
    context['contenuCommande'] = ContenuCommande.objects.all()

    return render(request, 'espace_admin/liste_commandes.html',context)

