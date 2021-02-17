from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import TypeProduit, Produit
from .forms import ProduitForm


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
    produit = Produit.objects.get(id_produit = idProduit)
    producteur = Personne.objects.get(id_personne = produit.id_producteur)
    context = {
        'leproduit': produit,
        'id': produit.id_produit
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

def ajout_quantite(request):
    template = loader.get_template('produit/ajout_quantite.html')
    return HttpResponse(template.render({},request))