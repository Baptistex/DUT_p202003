from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from .models import TypeProduit, Produit, Image
from espace_perso.models import Personne, Producteur, Adresse
from .forms import ProduitForm, ImageForm
from espace_perso.utils import great_circle_vec
from django.template.loader import render_to_string


# Create your views here.



def produit_django(request):
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
        print("hello")
        searchtext = request.POST.get("searchtext", None)
        print(searchtext)
        images_produit = Image.objects.filter(priorite=1).filter(produit__nom__icontains=searchtext)
        html = render_to_string(
            template_name="produit/produitsearch.html", 
            context={"lesproduits": images_produit, "MEDIA_URL" : "/media/"}
        )
        print(images_produit)
        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)


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
    images_produit = Image.objects.filter(priorite=1)
    print(images_produit)
    #Si l'utilisateur appuie sur le bouton, affiche que les producteurs dans un rayon de moins de 10km
    #TODO : Détecter un bouton en particulier, plutot que n'importe quel bouton/form
    if userCoordsSet and request.method == 'POST':
        for image in images_produit:        
            padresse = image.produit.producteur.adresse
            plat, plon = padresse.lat, padresse.lon
            distance = great_circle_vec(ulat, ulon, plat, plon)
            print(padresse, distance)
            if distance > 10000 :
                print(image.id)
                images_produit = images_produit.exclude(id=image.id)

    context = {
        'lesproduits': images_produit
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

    print("les images : ", table_images)

    context = {
        'leproduit': produit,
        'id': produit.produit_id,
        'producteur' : producteur,
        'lesImages' : table_images,
        'range' : range(produit.quantite),
        'qte' : produit.quantite,
        'notif10km' : notif10km,
    }
    return render(request, 'produit/description_prod.html', context)







def liste_produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def ajout_prod(request):
    personne_id = request.user.pk
    u = Producteur.objects.get(personne_ptr_id=personne_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.producteur = u
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/nouvelleimage')
    else:
        form = ProduitForm(initial ={'producteur': u})
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


def ajout_prod_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/accueilEspaceProducteur')
    else:
        form = ImageForm()
    return render(request, 'produit/ajout_image.html', {'form': form})

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
