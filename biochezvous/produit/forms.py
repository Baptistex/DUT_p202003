from django import forms
from django.forms import ModelForm
from .models import Image, TypeProduit, Categorie, Produit
from espace_perso.models import Producteur, Personne




class TypeProduitForm(ModelForm):
    class Meta:
        model = TypeProduit
        fields = ['nom', 'tva']
        

class CategorieForm(ModelForm):
    type_id = forms.ModelChoiceField(queryset=TypeProduit.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Type de produit")
    class Meta:
        model = Categorie
        fields = ['nom','type_id']


#A changer pour que le choix du producteur se fasse automatiquement
class ProduitForm(ModelForm):
    producteur = forms.ModelChoiceField(queryset=Producteur.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Nom du producteur")
    categorie_id = forms.ModelChoiceField(queryset=Categorie.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Nom de la categorie")

    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'unit', 'unit']

#Formulaire pour ajouter des images a un produit
class ImageForm(ModelForm):
    produit = forms.ModelChoiceField(queryset=Produit.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Produit à selectionner")
    class Meta:
        model = Image
        fields = ['image','produit']