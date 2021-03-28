from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import TypeProduit, Produit, Image
from espace_perso.models import Personne, Producteur
from .forms import ProduitForm, ImageForm
from espace_perso.utils import great_circle_vec


# Create your views here.



def produit_django(request):
    #Recuperation de toute la table personne dans une variable table_pers
    #  et passage a la template via context
    #TODO: Simplifier ce code une fois que la gestion de priorité sera ajoutée
    userCoordsSet = False
    if request.user.is_authenticated:
        user = request.user
        ulat, ulon = user.lat, user.lon
        if not ulat is None:
            userCoordsSet = True


    if request.method == 'POST':
        pass

    else: 
        pass
    table_image = Image.objects.select_related('produit').order_by('produit_id')
    produit_id_list = []
    image_id_list = []
    for i in table_image:
        #Si l'utilisateur n'est pas authentifié ou vient d'arriver sur la page, afficher tous les producteurs
        if not userCoordsSet or request.method == 'GET':
            if not i.produit_id in produit_id_list:
                produit_id_list.append(i.produit_id)
                image_id_list.append(i.id)
        #Si l'utilisateur appuie sur le bouton, affiche que les producteurs dans un rayon de moins de 10km
        else:
            plat, plon = i.produit.producteur.lat, i.produit.producteur.lon
            if not plat is None and not plon is None:
                distance = great_circle_vec(ulat, ulon, plat, plon)
                if distance<10000:
                    if not i.produit_id in produit_id_list:
                        produit_id_list.append(i.produit_id)
                        image_id_list.append(i.id)
            
    table_image = table_image.filter(id__in=image_id_list)
    
    images_produit = Image.objects.filter(priorite=1)

    context = {
        'lesproduits': images_produit
    }
    return render(request, 'produit/produit.html', context)




def produit(request, idProduit):
    #template = loader.get_template('produit/description_prod.html')
    # affichage de la description du produit
    userCoordsSet = False
    if request.user.is_authenticated:
        user = request.user
        ulat, ulon = user.lat, user.lon
        if not ulat is None:
            userCoordsSet = True

    produit = Produit.objects.get(produit_id = idProduit)
    producteur = produit.producteur

    notif10km = ""
    plat, plon = producteur.lat, producteur.lon
    if userCoordsSet and not plat is None and not plon is None:
        distance = great_circle_vec(ulat, ulon, plat, plon)
        if distance>10000:
            notif10km = "Ce produit appartient a un producteur qui est trop loin de chez vous"
            print("notif10km set")

    #producteur = produit.id_producteur
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
