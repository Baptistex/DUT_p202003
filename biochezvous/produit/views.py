from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.



def produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def liste_produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


def ajout_prod(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))
