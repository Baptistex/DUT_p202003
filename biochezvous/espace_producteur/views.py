from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Producteur

# Create your views here.


#view pour afficher le detail sur le producteur
def producteurs(request):
    template = loader.get_template('producteur/test_desc.html')
    return HttpResponse(template.render({},request))