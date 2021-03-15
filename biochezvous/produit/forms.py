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
    nom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-2 container-fluid'}))
    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(),
                                    to_field_name = 'categorie_id',
                                    empty_label="Nom de la categorie") 
    description=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-3 container-fluid'}))
    producteur = forms.ModelChoiceField(queryset=Producteur.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Nom du producteur")
    date=forms.CharField(initial='aaaa-mm-jj')
    class Meta:
        model = Produit
        fields = ['nom','quantite', 'prix', 'unit', 'description','producteur','categorie','quantite','date']
        

#Formulaire pour ajouter des images a un produit
class ImageForm(ModelForm):
    image=forms.ImageField(max_length=None,allow_empty_file=".jpg, .jpeg, .png")
    produit = forms.ModelChoiceField(queryset=Produit.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Produit à selectionner")
    class Meta:
        model = Image
        fields = ['image','produit']