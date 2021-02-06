from django import forms
from django.forms import ModelForm
from .models import TypeProduit, Categorie, Produit
from espace_perso.models import Producteur




class TypeProduitForm(ModelForm):
    class Meta:
        model = TypeProduit
        fields = ['nom', 'tva']
        

class CategorieForm(ModelForm):
    id_type = forms.ModelChoiceField(queryset=TypeProduit.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Type de produit")
    class Meta:
        model = Categorie
        fields = ['nom','id_type']


#A changer pour que le choix du producteur se fasse automatiquement
class ProduitForm(ModelForm):
    id_producteur = forms.ModelChoiceField(queryset=Producteur.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Nom du producteur")
    id_categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Nom de la categorie")

    class Meta:
        model = Produit
        fields = ['nom', 'description', 'prix', 'unit', 'unit']