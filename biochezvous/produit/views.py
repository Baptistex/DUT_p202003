from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from produit.models import TypeProduit, Produit


# Create your views here.



def produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def liste_produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def ajout_prod(request):
    template = loader.get_template('produit/ajout_produit.html')
    produit_exemple = TypeProduit(nom = "Patate", info = "Pomme de terre rouge", prix = 2.3, tva = 0.20, unit = False)
    produit_exemple.save()
    return HttpResponse(template.render({},request))
