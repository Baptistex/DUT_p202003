from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from produit.models import Produit

# Create your views here.

def accueil(request):
    template = loader.get_template('accueil/index.html')

    table_fraicheur = Produit.objects.order_by('date')[:6]

    context = {
        'lesfraicheurs': table_fraicheur
    }
    return HttpResponse(template.render({},request))