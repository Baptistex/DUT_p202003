from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from espace_perso.models import Personne
from .models import Demandes #importer modèle de 'espace_perso' - pas nécessaire de recréer modèle personne

#Accueil
def espace_admin(request):
    template = loader.get_template('espace_admin/accueil_admin.html')
    return HttpResponse(template.render({},request))

#Liste utilisateurs
def userlist(request):
    template = loader.get_template('espace_admin/userlist.html')
    table_pers = Personne.objects.all()
    context = {
        'userlist': table_pers
    }

    return HttpResponse(template.render(context,request))

def delete_user(request):
    if request.method == "GET":
        dest = Personne.objects.all()
        dest.delete()
        template = loader.get_template('espace_admin/userlist.html')
        table_pers = Personne.objects.all()
        context = {
            'userlist': table_pers
        }
    return HttpResponse(template.render(context,request))
    
def deleteOneUser(request,id):
    if request.method == "GET":
        dest = Personne.objects.get(personne_id = id)
        dest.delete()
        template = loader.get_template('espace_admin/userlist.html')
        table_pers = Personne.objects.all()
        context = {
            'userlist': table_pers
        }
    return HttpResponse(template.render(context,request))

#SAV
def util_aide(request):
    template = loader.get_template('espace_admin/aide.html')
    return render(request,'espace_admin/aide.html', {'dataDemandes': Demandes.objects.all()})
    
