from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import TypeProduit, Produit
from .forms import TypeProduitForm


# Create your views here.



def produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def liste_produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def ajout_prod(request):
    if request.method == 'POST':
        form = TypeProduitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/')
    else:
        form = TypeProduitForm()
    return render(request, 'produit/ajout_produit.html', {'form': form})

def ajout_quantite(request):
    template = loader.get_template('produit/ajout_quantite.html')
    return HttpResponse(template.render({},request))