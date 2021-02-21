from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import TypeProduit, Produit
from .forms import ProduitForm, ImageForm
from espace_perso.models import Personne


# Create your views here.





def produit_django(request):
    # template = loader.get_template('produit/produit.html')

    #Recuperation de toute la table personne dans une variable table_pers
    #  et passage a la template via context
    table_produits = Produit.objects.all()
    context = {
        'lesproduits': table_produits
    }
    return render(request, 'produit/produit.html', context)




def produit(request, idProduit):
    #template = loader.get_template('produit/description_prod.html')
    # affichage de la description du produit
    produit = Produit.objects.get(produit_id = idProduit)
    producteur = Personne.objects.get(personne_id = produit.producteur_id)
    #Un champ lié par clé étrangère peut être accédé comme ceci aussi:
    #La confusion vient du fait que le champ s'appelle id_producteur dans le modèle
    #Mais django ajoute le suffixe _id (donc id_producteur_id) dans la BDD
    #TODO (Baptiste sur master) : Renommer les champs FK pour retirer le id_
    #producteur = produit.id_producteur

    context = {
        'leproduit': produit,
        'id': produit.produit_id,
        'producteur' : producteur,
    }
    return render(request, 'produit/description_prod.html', context)







def liste_produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def ajout_prod(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/')
    else:
        form = ProduitForm()
    return render(request, 'produit/ajout_produit.html', {'form': form})


def ajout_prod_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/')
    else:
        form = ImageForm()
    return render(request, 'produit/ajout_produit.html', {'form': form})

def ajout_quantite(request):
    template = loader.get_template('produit/ajout_quantite.html')
    return HttpResponse(template.render({},request))