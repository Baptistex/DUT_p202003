from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import TypeProduit, Produit, Image, Panier
from espace_perso.forms import FormSelectionQuantite
from espace_perso.models import Personne, Producteur, Adresse
from .forms import ProduitForm, ImageForm, ContactForm
from espace_perso.utils import great_circle_vec
from django.core.mail import EmailMessage
from django.core.mail import send_mail, BadHeaderError
from espace_perso.models import Personne, Producteur, Adresse, Preference
from .forms import ProduitForm, ImageForm, CategorieForm,TypeProduitForm
from espace_perso.utils import great_circle_vec
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required


# Create your views here.



def catalogue(request):
    """
    Vue qui permet d'afficher les differents produits mis en vente sur le site
    Un bouton permet de filtrer les produits à ceux étant vendus par des producteurs proches

    Args:

    Returns:
        lesproduits : liste d'images desquelles ont peut obtenir les produits associés

    Authors:
        Baptiste Alix, Paul Breton
    """
    if request.is_ajax():
        userCoordsSet = False
        ulat, ulon = 0, 0
        if request.user.is_authenticated:
            user = request.user
            try : 
                ulat, ulon = user.adresse.lat, user.adresse.lon
                if not (ulat is None or ulon is None) :
                    userCoordsSet = True
            except Adresse.DoesNotExist:
                pass

        boutondistance = True if (request.POST.get("boutondistance", None) == "true") else False
        searchtext = request.POST.get("searchtext", None)

        if searchtext == "":
            images_produit = Image.objects.filter(priorite=1)
        else :
            images_produit = Image.objects.filter(priorite=1).filter(produit__nom__icontains=searchtext)

        if boutondistance :
            for image in images_produit:        
                padresse = image.produit.producteur.adresse
                plat, plon = padresse.lat, padresse.lon
                distance = great_circle_vec(ulat, ulon, plat, plon)
                if distance > 10000 :
                    images_produit = images_produit.exclude(id=image.id)

        html = render_to_string(
            template_name="produit/produitsearch.html", 
            context={"lesproduits": images_produit, "MEDIA_URL" : "/media/"},
            request=request
        )
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)

    images_produit = Image.objects.filter(priorite=1)
    if request.user.is_authenticated :
        mesPref = Preference.objects.filter(personne=request.user)
        produits_pref = Produit.objects.filter(preference__in=mesPref)
    else : 
        produits_pref = ""
    context = {
        'lesproduits': images_produit,
        'produits_pref' : produits_pref,
    }
    return render(request, 'produit/produit.html', context)




def produit(request, idProduit):
    """
    Vue qui permet d'afficher un produit et ses informations
    
    Args:

    Returns:
        leproduit : le produit
        id : identifiant du produit
        producteur : producteur qui met en vente le produit
        lesImages : les images du produit
        range : range(produit.quantite)
        qte : quantite du produit
        notif10km : Un avertissement si le produit est trop loin ou que l'adresse de l'utilisateur n'a pas été ajoutée
    Authors:
        Baptiste Alix, Paul Breton
    """
    userCoordsSet = False
    notif10km = ""
    ulat, ulon = 0, 0
    if request.user.is_authenticated:
        user = request.user
        try : 
            ulat, ulon = user.adresse.lat, user.adresse.lon
            if not (ulat is None or ulon is None) :
                userCoordsSet = True
        except Adresse.DoesNotExist:
            notif10km = "Vous n'avez pas spécifié d'adresse sur votre profil."

    produit = Produit.objects.get(produit_id = idProduit)
    producteur = produit.producteur
        
    plat, plon = producteur.adresse.lat, producteur.adresse.lon
    if userCoordsSet and not plat is None and not plon is None:
        distance = great_circle_vec(ulat, ulon, plat, plon)
        if distance>10000:
            notif10km = "Ce produit appartient a un producteur qui est trop loin de chez vous"
            print("notif10km set")

    table_images = Image.objects.filter(produit = produit)

    

    if request.method == 'POST':
        form = FormSelectionQuantite(request.POST)
            
        if form.is_valid():
            if request.user.is_authenticated:
                mon_panier_prod = Panier.objects.all().filter(produit=produit, personne=request.user).values('quantite')
                
                if mon_panier_prod.exists():
                    qte = int(request.POST['quantite']) + mon_panier_prod[0]['quantite']
                    Panier.objects.filter(produit=produit, personne=request.user).update(quantite = qte)
                else:
                    p = Panier(personne=request.user, produit=produit, quantite=request.POST['quantite'])
                    p.save()
                reste = int(produit.quantite) - int(request.POST['quantite'])
                Produit.objects.filter(produit_id = idProduit).update(quantite = reste)
                return redirect('panier')
            else: 
                return redirect('connexion')
    else:
        form = FormSelectionQuantite()
    
    context = {
        'leproduit': produit,
        'id': produit.produit_id,
        'producteur' : producteur,
        'lesImages' : table_images,
        'range' : range(produit.quantite),
        'qte' : produit.quantite,
        'form' : form,
        'notif10km' : notif10km,
    }
    return render(request, 'produit/description_prod.html', context)







def liste_produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def ajout_prod(request):
    try:
        personne_id = request.user.pk
        adresse = Adresse.objects.get(personne_id=personne_id)
        u = Producteur.objects.get(personne_ptr_id=personne_id)
        if(adresse.lat !=0 and adresse.lon !=0):
            if request.method == 'POST':
                form = ProduitForm(request.POST, request.FILES)
                if form.is_valid():
                    instance = form.save(commit=False)
                    instance.producteur = u
                    instance.save()
                    return redirect('aff_prod')
            else:
                form = ProduitForm()
        else:
            return redirect('ajout_prod_adresse')
    except  Adresse.DoesNotExist:
        return redirect('ajout_prod_adresse')
    return render(request, 'produit/ajout_produit.html', {'form': form})

def aff_prod(request):
    #u = request.user
    personne_id = request.user.personne_id
    template = loader.get_template('produit/suppr_produit.html')
    table_prod = Produit.objects.filter(producteur_id=personne_id)
    context = { 
        'prodlist': table_prod
    }
    return HttpResponse(template.render(context,request))


@permission_required ('espace_perso.can_view_espace_producteur', login_url='connexion')
def ajout_prod_image(request, id_produit):
    """
    Vue qui permet de modifier les images d'un produit, par le producteur.
    Lui permet d'ajouter des images, les supprimer, et de changer l'ordre de priorité.

    Args : id_produit : clé primaire de l'instance de Produit.

    Returns: une vue, avec le context suivant : 
        form : le formulaire
        lesproduits : liste d'images desquelles ont peut obtenir les produits associés
        id_produit : clé primaire de l'instance de Produit.

    Authors:
        Baptiste Alix
    """
    u = request.user.producteur

    #Redirection de du producteur si le produit ne lui appartient pas
    if Produit.objects.filter(producteur=u).filter(pk=id_produit).count() == 0:
        return redirect('producteur', idProducteur=u.pk)

    images_produits = Image.objects.filter(produit_id = id_produit).order_by('priorite')
    if request.method == 'POST' and images_produits.count() <3:
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(priorite=images_produits.count()+1, produit_id=id_produit)
            instance.save()
            return redirect('ajout_prod_image', id_produit)
    else:
        form = ImageForm()
    context = {
        'form' : form,
        'images_produits' : images_produits,
        'id_produit' : id_produit
    }
    return render(request, 'produit/ajout_image.html', context)

@permission_required ('espace_perso.can_view_espace_producteur', login_url='connexion')
def suppr_prod_image(request, id_image):
    """
    Vue qui permet de supprimer une image de produit

    Args : id_image : clé primaire de l'instance de Image.

    Returns: une redirection vers ajout_prod_image(id_produit)
        avec id_produit la clé primaire de l'instance de Produit


    Authors:
        Baptiste Alix
    """
    u = request.user.producteur
    image = Image.objects.get(pk=id_image)
    #Redirection de du producteur si le produit ne lui appartient pas
    if image.produit.producteur!=u:
        return redirect('producteur', idProducteur=u.pk)
    id_produit = image.produit.pk
    image.delete()
    image_list = Image.objects.filter(produit_id=id_produit).order_by('priorite')
    count = 1
    for image in image_list:
        if image.priorite != count:
            image.priorite -= 1
            image.save()
        count+=1
    return redirect('ajout_prod_image', id_produit)

def update_image_priorite(request):
    """
    Vue qui de mettre à jour les priorité des images d'un produit.
    Fonctionne en ajax

    Authors:
        Baptiste Alix
    """
    if request.is_ajax():
        id_produit = request.POST.get("id_produit", None)
        order = request.POST.get("order", None)
        if Produit.objects.filter(producteur=request.user.producteur).filter(produit_id=id_produit).count()>0 : 
            order_list = order.split(',')
            image_list = Image.objects.filter(produit_id=id_produit).order_by('priorite')
            count = 1
            for image in image_list:
                image.priorite = order_list.index(str(count))+1
                count += 1
                image.save()
        return HttpResponse()
    else : 
        return HttpResponseNotFound("Page non trouvée")
    
def ajout_quantite(request):
    template = loader.get_template('produit/ajout_quantite.html')
    return HttpResponse(template.render({},request))
    

def deleteOneProd(request,id):
    if request.method == "GET":
        personne_id = request.user.personne_id
        dest = Produit.objects.get(produit_id = id)
        dest.delete()
        template = loader.get_template('espace_perso/wip_userlist.html')
        table_prod = Produit.objects.filter(producteur_id=personne_id)
        context = { 
            'prodlist': table_prod
        }
    return HttpResponse(template.render(context,request))

def email(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['biochezvous.iut@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('thanks')
    return render(request, "produit/base.html", {'form': form})

def thanks(request):
    return HttpResponse('Merci pour votre message')
def ajout_categorie(request):
    if request.method == 'POST':
        form = CategorieForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return HttpResponseRedirect('/accueilEspaceProducteur')
    else:
        form = CategorieForm()
    return render(request, 'produit/categorie.html', {'form': form})
 
def ajout_preference(request, produit):
    
    if request.user.is_authenticated:
        preference = Preference.objects.filter(produit=Produit.objects.get(produit_id=produit), personne=request.user)
        pref = Preference(produit=Produit.objects.get(produit_id=produit), personne=request.user)
        if preference.exists():
            preference.delete()
        else:            
            pref.save()
    else:
        return redirect('/connexion')

    return HttpResponseRedirect('/produits')

def addType(request):
    if request.method == 'POST':
        form = TypeProduitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            #TODO: changer la redirection
            return redirect('espace_admin')
    else:
        form = TypeProduitForm()
    return render(request, 'produit/ajout_typeProduit.html', {'form': form})
