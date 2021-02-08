from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
# Create your views here.

def espace_admin(request):
    template = loader.get_template('espace_admin/accueil_admin.html')
    return HttpResponse(template.render({},request))

def util_inscris(request):
    template = loader.get_template('espace_admin/util_inscris.html')
    return HttpResponse(template.render({},request))