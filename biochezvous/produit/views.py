from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
<<<<<<< HEAD
from .models import TypeProduit, Produit, Image
from espace_perso.models import Personne
from .forms import ProduitForm
=======
from .models import Image, TypeProduit, Produit
from .forms import ProduitForm, ImageForm
from espace_perso.models import Personne
>>>>>>> e9a76fc391ad155685c9d41ae9e9cc25bac8ae52


# Create your views here.



def produit_django(request):
    #Recuperation de toute la table personne dans une variable table_pers
    #  et passage a la template via context
    #TODO: Simplifier ce code une fois que la gestion de priorité sera ajoutée
    table_image = Image.objects.select_related('produit').order_by('produit_id')
    produit_id_list = []
    for i in table_image:
        if not i.produit_id in produit_id_list:
            produit_id_list.append(i.produit_id)
        else:
            table_image.delete(i)
        
    print(table_image)
    context = {
        'lesproduits': table_image
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