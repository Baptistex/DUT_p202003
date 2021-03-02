from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader


# Create your views here.


#view pour afficher le detail sur le producteur
def producteurs(request):
   
    context = {
        'mesProduits': '',
    }
    return render(request, 'producteur/description_producteur.html', context)