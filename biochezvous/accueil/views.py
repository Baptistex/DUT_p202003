from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from produit.models import Produit, Image
from espace_perso.models import Producteur, Personne

# Create your views here.

def accueil(request):
    images_produit = Image.objects.filter(priorite=1)[:6]
    producteur = Producteur.objects.all()
    produit = Produit.objects.all()
    client = Personne.objects.all()
    context = {
        'lesfraicheurs': images_produit,
        'nb_producteur' : len(producteur),
        'nb_recette' : 0,
        'nb_happyClient': len(client),
        'nb_produit':len(produit),
    }
    return render(request, 'accueil/index.html', context)


def propos(request):
    template = loader.get_template('accueil/propos.html')
    return HttpResponse(template.render({},request))
    return HttpResponse(template.render(context,request))
