from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import TypeProduit, Produit, Image
from espace_perso.models import Personne, Producteur
from .forms import ProduitForm, ImageForm



# Create your views here.



def produit_django(request):
    #Recuperation de toute la table personne dans une variable table_pers
    #  et passage a la template via context
    #TODO: Simplifier ce code une fois que la gestion de priorité sera ajoutée
    table_image = Image.objects.select_related('produit').order_by('produit_id')
    produit_id_list = []
    image_id_list = []
    for i in table_image:
        if not i.produit_id in produit_id_list:
            produit_id_list.append(i.produit_id)
            image_id_list.append(i.id)
            
    table_image = table_image.filter(id__in=image_id_list)
    
    context = {
        'lesproduits': table_image
    }
    return render(request, 'produit/produit.html', context)




def produit(request, idProduit):
    #template = loader.get_template('produit/description_prod.html')
    # affichage de la description du produit
    produit = Produit.objects.get(produit_id = idProduit)
    producteur = Personne.objects.get(personne_id = produit.producteur_id)
    #Un champ lié par clé étrangère peut être accédé comme ceci aussi:
    #La confusion vient du fait que le champ s'appelle id_producteur dans le modèle
    #Mais django ajoute le suffixe _id (donc id_producteur_id) dans la BDD
    #TODO (Baptiste sur master) : Renommer les champs FK pour retirer le id_
    #producteur = produit.id_producteur
    table_images = Image.objects.filter(produit = produit)

    print("les images : ", table_images)
   
    context = {
        'leproduit': produit,
        'id': produit.produit_id,
        'producteur' : producteur,
        'lesImages' : table_images,
        'range' : range(produit.quantite),
        'qte' : produit.quantite,
    }
    return render(request, 'produit/description_prod.html', context)







def liste_produit(request):
    template = loader.get_template('produit/produits.html')
    return HttpResponse(template.render({},request))


#@permission_required ('espace_perso.can_view_espace_perso', login_url='connexion')
def ajout_prod(request):
    #personne_id = request.user.personne_id
    #personne_ptr_id = request.user.personne_ptr_id
    #u = Producteur.objects.get(personne_ptr_id=personne_id)
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/nouvelleimage')
    else:
        form = ProduitForm()
    return render(request, 'produit/ajout_produit.html', {'form': form})


def ajout_prod_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            instance.save()
            #TODO: changer la redirection
            return HttpResponseRedirect('/accueilEspaceProducteur')
    else:
        form = ImageForm()
    return render(request, 'produit/ajout_image.html', {'form': form})

def ajout_quantite(request):
    template = loader.get_template('produit/ajout_quantite.html')
    return HttpResponse(template.render({},request))
    