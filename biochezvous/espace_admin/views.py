from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from espace_perso.models import Personne #importer modèle de 'espace_perso' - pas nécessaire de recréer modèle personne

def espace_admin(request):
    template = loader.get_template('espace_admin/accueil_admin.html')
    return HttpResponse(template.render({},request))

def util_inscris(request):
    
    #Tableau des producteurs
    table_prod = Personne.objects.filter(groups__name='producteur')

    #Tableau des consommateurs
    table_conso = Personne.objects.filter(groups__name='utilisateur')

    return render(request, 'espace_admin/util_inscris.html',{'listeProd':table_prod,'listeConso':table_conso})