from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from espace_admin.models import Demandes
from .models import Utilisateur,Personne, Producteur, Adresse
from espace_perso.forms import FormInscriptionProd, FormAide
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
from .forms import FormInscription, FormConnexion, FormDataModification, FormInscriptionUser #, Suppression
from .utils import send_mail_pay
from .utils import send_mail_cmd
from .tokens import account_activation_token
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
#from .forms import FormInscription, FormConnexion, FormDataModification, FormInscriptionUser, FormQuantitePanier
from .forms import FormInscription, FormConnexion, FormDataModification, FormInscriptionUser, FormDataModifProd, AdresseModifForm
from produit.models import Commande, ContenuCommande, Panier, Produit
from produit.models import Image
from datetime import datetime
from django.utils.html import strip_tags


from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


# Create your views here.





    
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

def send_mail_commande(request, commande_id):
    if Commande.objects.filter(produits__in=request.user.producteur.produit_set.all()).filter(commande_id=commande_id).count() <= 0 :
        redirect("accueil")
    else:
        com = Commande.objects.get(commande_id=commande_id)
        com.statut = 1
        com.save()
        user = Personne.objects.get(commandes__exact=commande_id)
        send_mail_cmd(user, commande_id)
    return redirect('commandeProducteur')

    
def inscription_user(request):
    if request.method == 'POST':
        form = FormInscriptionUser(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Bienvenue'
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            text_content = strip_tags(message)
            to_email = form.cleaned_data.get('mail')
            email = EmailMultiAlternatives(
                        mail_subject, message, to=[to_email]
            )
            email.attach_alternative(message, "text/html")
            email.send()
            return HttpResponse('Veuillez confirmer votre adresse mail pour finaliser votre inscription')
            #TODO: changer la redirection
            return HttpResponseRedirect('/connexion')
    else:
        form = FormInscriptionUser()
    #TODO : un template propre à chaque type d'inscription
    return render(request, 'espace_perso/inscription_prod.html', {'form' : form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Personne.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        redirect('/connexion')
        return HttpResponse("Merci d'avoir confirmer votre adresse email. Maintenant vous pouvez vous connecter à votre compte.")
    else:
        print(token)
        return HttpResponse("Le lien d'activation n'est pas valide!")

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
    if request.method == 'POST':
        form = FormConnexion(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return redirect('accueil')

    else:
        form = FormConnexion()
    return render(request, 'espace_perso/connexion_prod.html', {'form' : form, 'verif_connexion' : verif_connexion})


def deconnexion(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('accueil')
 
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
    if Producteur.objects.filter(personne_ptr_id=request.user.personne_id).count() > 0 :
        return render(request, 'espace_perso/espaceProd.html', context)

    else : 
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
        Justine Fouillé, Melvin
    """
    u = request.user
    #Si l'user est un producteur : 
    if Producteur.objects.filter(personne_ptr_id=u.personne_id).count() > 0 :
        form = FormDataModifProd(instance=u.producteur)
        if request.method == 'POST' :
            form = FormDataModifProd(request.POST, request.FILES, instance=u.producteur)
            if form.is_valid():
                form.save()
                return redirect('espacePerso')
        context = {'form':form}
        return render(request, 'espace_perso/informationProd.html', context)

    #Sinon : 
    else :
        form = FormDataModification(instance=u)
        if request.method == 'POST' :
            form = FormDataModification(request.POST, instance=u)
            if form.is_valid():
                form.save()
                return redirect('espacePerso')
        context = {'formG':form}
        return render(request, 'espace_perso/informationPerso.html', context)


def aide(request):
    if request.method == "POST":
        form = FormAide(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/aide')
    else:
        form = FormAide()
    return render(request,'espace_perso/demande_aide.html', {'form':form})
#
# 
# espace PRODUCTEUR
#
#
#view pour afficher le detail sur le producteur
def producteur(request, idProducteur):
    
    producteur = Producteur.objects.get(personne_id = idProducteur)
    images_produit = Image.objects.filter(produit_id__in=Produit.objects.filter(producteur=producteur)).filter(priorite=1)

    context = {
        'leproducteur' : producteur,
        'mesProduits': images_produit,
    }
    return render(request, 'espace_perso/description_producteur.html', context)
    


def espacePersoProd(request):
    
    personne_id = request.user.personne_id
    u = Producteur.objects.get(personne_ptr_id=personne_id)
    form = FormDataModifProd(instance=u)
    if request.method == 'POST':
        form = FormDataModifProd(request.POST, request.FILES, instance=u)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/profil/adresse/edit')
    return render(request, 'espace_perso/espacePersoProd.html', {'form': form})



def ajout_prod_adresse(request):
    if request.method == 'POST':
        try:
            form = AdresseModifForm(request.POST, instance=request.user.adresse)
        except Adresse.DoesNotExist: 
            form = AdresseModifForm(request.POST)
        if form.is_valid():
            adresse = form.save(commit=False)
            adresse.personne = request.user 
            adresse.save()
            return redirect('espacePerso')
    else:
        try : 
            form = AdresseModifForm(instance = request.user.adresse)
        except Adresse.DoesNotExist: 
            form = AdresseModifForm()
    return render(request, 'espace_perso/ajout_adresse.html', {'form': form})


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

    panier = Panier.objects.filter(personne_id=personne_id)
    montantP = 0 
    #calcul du montant
    for prod in panier:
        montantP = montantP + (prod.produit.prix * prod.quantite)

    context['panier'] = panier
    context['montant'] = round(montantP,2)

    return render(request, 'espace_perso/panier.html',context)


#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def suppressionPanier(request, id):
    """
    Supprimer un élement du panier

    Args:
        id : c'est l'id du produit à terminer

    Returns:
        redirige vers la vue panier

    Authors:
        Justine Fouillé
    """
    #gérer le fait que ce soit les articles pour l'utilisateur donné 
    personne_id = request.user.personne_id
    panier = Panier.objects.filter(personne_id=personne_id)  
    produitDuPanier = panier.get(produit_id=id)
    produit = Produit.objects.get(produit_id=id)
    produit.quantite = produit.quantite + produitDuPanier.quantite
    produit.save()
    produitDuPanier.delete()
    return redirect('panier')

#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def varierArticlePanier(request):
    if request.is_ajax():
        id = request.POST.get("id_produit", None)
        amount = int(request.POST.get("amount", None))
        suppression = 0
        try :
            item = Panier.objects.filter(personne=request.user).get(produit_id=id)
            if amount == -1 :
                if item.quantite <= 1:
                    suppression = 1
                else : 
                    item.quantite -= 1

            if amount == 1 :
                if item.quantite >= item.produit.quantite:
                    pass #TODO : Envoyer un avertissement, maximum atteint
                else:
                    item.quantite += 1
            item.save()
            data = {
                'quantite' : item.quantite,
                'suppression' : suppression
            }
        except : 
            suppression = 2 
            data = {
                'quantite' : 0,
                'suppression' : suppression
            }
        

        
        return JsonResponse(data=data, safe=False)
    else : 
        redirect('accueil')

def decrementerArticlePanier(request, id):
    pass

#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def incrementerArticlePanier(request, id):

    personne_id = request.user.personne_id
    panier = Panier.objects.filter(personne_id=personne_id)  
    produitDuPanier = panier.get(produit_id=id)
    stockArticle = Produit.objects.get(produit_id=id)

    if (produitDuPanier.quantite >= stockArticle.quantite):
        # cas où la personne veut commander + que en stock ???
        messages.error(request, "Il n'y a pas assez de stocks pour le nombre d'articles que vous vouez commander")
         
    else:
        produitDuPanier.quantite += 1
        produitDuPanier.save()
        return redirect('panier')

def commander(request):

    context = {}
    personne_id = request.user.personne_id
    adresses = Adresse.objects.filter(personne_id=personne_id)
    if (len(adresses)==0):
        messages.error(request, "Vous devez renseigner votre adresse avant de passer commande. Vous pouvez le faire depuis votre espace personnel")
        return redirect('panier')
    else:
        panier = Panier.objects.filter(personne_id=personne_id)
        montantP = 0 
        producteurs = Producteur.objects.filter(produit__in=Produit.objects.filter(panier__in=panier))

        for producteur in producteurs:
            u = producteur
            produits = Panier.objects.all().filter(produit_id__in=u.produit_set.all())
            for prod in produits:
                montantP = montantP + (prod.produit.prix * prod.quantite)
            c = Commande(date=datetime.now(), statut=0, montant=montantP,personne_id=personne_id)
            c.save()
            produits = Panier.objects.all().filter(produit_id__in=u.produit_set.all())
            for prod in produits:
                produit = ContenuCommande(quantite=prod.quantite, commande_id=c.commande_id, produit_id=prod.produit_id)
                produit.save()
                prod.delete()
                montantP = 0
        return redirect('listeCommande')

def commanderEncore(request, id):
    context = {}
    personne_id = request.user.personne_id
    panier = Panier.objects.filter(personne_id=personne_id)

    if not panier:  
        commande = Commande.objects.get(commande_id=id)
        contenuCommande = ContenuCommande.objects.filter(commande_id=id)
        #Mettre le contenu de panier dans ContenuCommande 
        for prod in contenuCommande :
            produit = Panier(quantite=prod.quantite, personne_id=personne_id, produit_id=prod.produit_id)
            produit.save()

        #NE PAS OUBLIER LES VÉRIFICATION
    
        #send_mail_pay(request)
        messages.success(request, "Le contenu de votre commande a bien été ajouté")
        return redirect('panier')
    messages.error(request, "Il y a déjà des articles dans votre panier. Vous devez d'abord appuyer sur le bouton commander encore de la commande que vous souhaiter acheter à nouveau avant de rajouter de nouveaux articles à votre panier.")
    #NE PAS OUBLIER LES VÉRIFICATION

    send_mail_pay(request)
    return redirect('listeCommande')
    


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



def PDF(request, id):
    context = {}
    context['contenuCommande'] = ContenuCommande.objects.filter(commande_id=id)
    context['Commande'] = Commande.objects.get(commande_id=id)
    context['client'] = request.user
    pdf = render_to_pdf('espace_perso/pdf_template.html', context)

    return HttpResponse(pdf, content_type='application/pdf')

#Opens up page as PDF
class ViewPDF(View):

	def get(self, request, *args, **kwargs):
		pdf = render_to_pdf('espace_perso/pdf_template.html', commande)
		return HttpResponse(pdf, content_type='application/pdf')

#Automaticly downloads to PDF file
class DownloadPDF(View):
	def get(self, request, *args, **kwargs):
		
		pdf = render_to_pdf('espace_perso/pdf_template.html', data)

		response = HttpResponse(pdf, content_type='application/pdf')
		filename = "facture.pdf"
		content = "attachment; filename='\%s\'" %(filename)
		response['Content-Disposition'] = content
		return response

def index(request):
	context = {}
	return render(request, 'espace_perso/test.html', context)


def commandeProducteur(request):
    context = {}
    template = loader.get_template('espace_perso/commandeProd.html')
    u = request.user.producteur
    cont=ContenuCommande.objects.all().filter(produit_id__in=u.produit_set.all())
    listeCommandes = []
    listeproduits = []
    for c in cont:
        commandes=Commande.objects.all().filter(commande_id=c.commande_id)  
        for cmd in commandes:
            if ((cmd.statut == 0) or (cmd.statut == 1)) :
                listeproduits.append(c)
                if (cmd not in listeCommandes):
                    listeCommandes.append(cmd)
    
    context['listeproduits'] = listeproduits
    context['listecommandes'] = listeCommandes

    return HttpResponse(template.render(context,request))



def terminerCommande(request, commande_id):
    com = Commande.objects.get(commande_id=commande_id)
    com.statut = 2
    com.save()
    return redirect('commandeProducteur')

