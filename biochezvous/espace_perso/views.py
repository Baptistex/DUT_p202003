from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from collections import namedtuple
from django.template import loader
from django.contrib.auth import authenticate, login, logout
from espace_admin.models import Demandes
from .models import Utilisateur,Personne, Producteur, Adresse
from espace_perso.forms import FormInscriptionProd, FormAide
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group, Permission
#from .forms import FormInscription, FormConnexion, FormDataModification, FormInscriptionUser, FormQuantitePanier
from .forms import FormInscription, FormConnexion, FormDataModification, FormInscriptionUser, FormDataModifProd, AdresseModifForm
from produit.models import Commande, ContenuCommande, Panier, Produit
from produit.models import Image
from datetime import datetime


from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa


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
                return redirect('')

    else:
        form = FormConnexion()
    return render(request, 'espace_perso/connexion_prod.html', {'form' : form, 'verif_connexion' : verif_connexion})


def deconnexion(request):
    template = loader.get_template('espace_perso/deconnexion.html')
    if request.user.is_authenticated:
        logout(request)
    return HttpResponse(template.render({},request))

#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
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
    #TODO Vérifier la vérification automatique des champs du formulaire
    personne_id = request.user.personne_id
    u = Personne.objects.get(personne_id=personne_id)
    formG = FormDataModification(instance=u)
    u = request.user
    form = FormDataModification(instance=u)
    if request.method == 'POST' :
        formG = FormDataModification(request.POST, instance=u)
        if formG.is_valid():
            formG.save()
    context = {'formG':formG}

    return render(request, 'espace_perso/informationPerso.html', context)

#   Utilisez ces fonctions (en remplaçant name et codename) pour ajouter une permission à un groupe
#def update_Permissions(request):
#    prod_group, created = Group.objects.get_or_create(name='producteur')
#    print(prod_group.permissions)
#    prod_group.permissions.add(
#        Permission.objects.get(codename='can_view_espace_perso')
#    )

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
    

@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def espace_producteur(request):
    template = loader.get_template('espace_perso/accueil_espaceProd.html')
    return HttpResponse(template.render({},request))
    

    

def espacePersoProd(request):

    personne_id = request.user.personne_id
    u = Producteur.objects.get(personne_ptr_id=personne_id)
    form = FormDataModifProd(instance=u)
    if request.method == 'POST':
        form = FormDataModifProd(request.POST, request.FILES, instance=u)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/nouvelleAdresse')
    return render(request, 'espace_perso/espacePersoProd.html', {'form': form})

def ajout_prod_adresse(request):
    if request.method == 'POST':
        form = AdresseModifForm(request.POST, instance=request.user.adresse)
        if form.is_valid():
            adresse = form.save(commit=False)
            adresse.personne = request.user 
            adresse.save()
            return HttpResponseRedirect('/accueilEspaceProducteur')
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
    context['montant'] = montantP

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
def decrementerArticlePanier(request, id):

    personne_id = request.user.personne_id
    panier = Panier.objects.filter(personne_id=personne_id)  
    produit = panier.get(produit_id=id)

    if (produit.quantite == 1):
        return redirect('suppressionPanier', id=id)
    else:
        produit.quantite -= 1
        produit.save()

    return redirect('panier')


#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def incrementerArticlePanier(request, id):

    personne_id = request.user.personne_id
    panier = Panier.objects.filter(personne_id=personne_id)  
    produitDuPanier = panier.get(produit_id=id)
    stockArticle = Produit.objects.get(produit_id=id)

    if (produitDuPanier.quantite >= stockArticle.quantite):
        #TODO : comment gérer le cas où la personne veut commander + que en stock ???
        print("trop")  
    else:
        produitDuPanier.quantite += 1
        produitDuPanier.save()
        return redirect('panier')

def commander(request):
    
    context = {}
    personne_id = request.user.personne_id
    panier = Panier.objects.filter(personne_id=personne_id)
    montantP = 0 
    #calcul du montant
    for prod in panier:
        montantP = montantP + (prod.produit.prix * prod.quantite)
    
    #Créer une commande dans Commande
    c = Commande(date=datetime.now(), statut=0, montant=montantP,personne_id=personne_id)
    c.save()

    #Mettre le contenu de panier dans ContenuCommande
    
    for prod in panier:
        produit = ContenuCommande(quantite=prod.quantite, commande_id=c.commande_id, produit_id=prod.produit_id)
        produit.save()
        #Vider le contenu de panier
        prod.delete()

    #NE PAS OUBLIER LES VÉRIFICATION
    
    #send_mail_pay(request)
    return redirect('listeCommande')
    #u = Personne.objects.get(personne_id=personne_id)
    #print(u.Commande_set(related_name))

    #contenuCommande = ContenuCommande.objects.filter(commande_id=id)
    #context['Commande'] = Commande.objects.get(commande_id=id)
    #Commande.objects.create()
    #context = {}
    #personne_id = request.user.personne_id
    
    #panier = Panier.objects.filter(personne_id=personne_id)
    #for prod in panier:
        #ContenuCommande.objects.create(prod)  
    #return render(request, 'espace_perso/listeCommande.html',context)


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None

data = {
	"company": "Dennnis Ivanov Company",
	"address": "123 Street name",
	"city": "Vancouver",
	"state": "WA",
	"zipcode": "98663",


	"phone": "555-555-2345",
	"email": "youremail@dennisivy.com",
	"website": "dennisivy.com",
	}



def PDF(request, id):
    context = {}
    context['contenuCommande'] = ContenuCommande.objects.filter(commande_id=id)
    context['Commande'] = Commande.objects.get(commande_id=id)
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
    template = loader.get_template('espace_perso/commandeProd.html')
    u = request.user.producteur
    cont=ContenuCommande.objects.all().filter(produit_id__in=u.produit_set.all())
    context = {
        'comlist': cont
    }
    return HttpResponse(template.render(context,request))
