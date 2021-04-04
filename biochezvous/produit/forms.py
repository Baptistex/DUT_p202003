from django import forms
from django.forms import ModelForm
from .models import Image, TypeProduit, Categorie, Produit
from espace_perso.models import Producteur, Personne
from PIL import Image as PILImage



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
    nom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    unit=forms.CharField(initial='(ex:Kg)',label="Unité du produit",widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-12 '}))
    date=forms.CharField(initial='aaaa-mm-jj',widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))

    #TODO : modifier la foreignkey du modele produit 


    categorie = forms.ModelChoiceField(queryset=Categorie.objects.all(),
                                    to_field_name = 'nom',
                                    empty_label="Nom de la categorie",)                                
    
    class Meta:
        model = Produit
        fields = ['nom','quantite', 'prix', 'unit', 'description','categorie','quantite','date']
        

#Formulaire pour ajouter des images a un produit
class ImageForm(ModelForm):
    image=forms.ImageField(max_length=None,allow_empty_file=".jpg, .jpeg, .png")
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Image
        fields = ['image', 'x', 'y', 'width', 'height']
    def save(self, priorite, produit_id):

        instance = super(ImageForm, self).save(commit=False)
        instance.priorite = priorite
        instance.produit_id = produit_id
        
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        image = PILImage.open(instance.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), PILImage.ANTIALIAS)
        instance.save()
        resized_image.save(instance.image.path)
        return instance



class CategorieForm(ModelForm):
    nom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    typeProduit = forms.ModelChoiceField(queryset=TypeProduit.objects.all(),
                                    to_field_name = 'nom',
                                    label="Type de produit",
                                    empty_label="Categorie à selectionner")
    class Meta:
        model=Categorie
        fields = ['nom','typeProduit']

class ContactForm(forms.Form):
    from_email = forms.EmailField(label='',widget=forms.TextInput(attrs={'placeholder':'Votre email'}), required=True)
    subject = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Objet'}), required=True)
    message = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder':'Message'}))