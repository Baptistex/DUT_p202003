from django import forms
from django.forms import ModelForm
from .models import Utilisateur, Personne, Producteur
from espace_admin.models import Demandes
from produit.models import Image
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .utils import getCoords
from .models import Adresse
from produit.models import Produit
from PIL import Image as PILImage



class FormInscription(UserCreationForm):
    
    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel']

class FormConnexion(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 container-fluid'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 container-fluid','type':'password'}))
    class Meta:
        model = Personne
        fields = ['username', 'password']

class FormInscriptionProd(UserCreationForm):
    nom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    prenom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    mail=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    num_tel=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-12 '}))
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    image=forms.ImageField(max_length=None,allow_empty_file=".jpg, .jpeg, .png", required=False)

    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)
    def save(self):
        user = super(FormInscriptionProd, self).save(commit=False)
        prod_group, created = Group.objects.get_or_create(name='producteur')
        #TODO : mettre confirmation a False
        user.confirmation = True
        user.newsletter = True
        user.save()
        user.groups.add(prod_group)
        if created:
            permissions_producteur = Permission.objects.filter(content_type=ContentType.objects.get(app_label='espace_perso', model='producteur').id)
            prod_group.permissions.set(permissions_producteur)
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if x==None or y==None or w==None or h==None :
            x, y, w, h = 0, 0, 100, 100
        image = PILImage.open(user.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), PILImage.ANTIALIAS)
        user.save()
        resized_image.save(user.image.path)
        return user
    class Meta:
        model = Producteur
        fields = ['nom', 'prenom', 'mail', 'num_tel','description','image','iban', 'x', 'y', 'width', 'height']

class FormInscriptionUser(UserCreationForm):
    
    nom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    prenom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    mail=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    num_tel=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    def save(self):
        user = super().save(commit=False)
        user_group, created = Group.objects.get_or_create(name='utilisateur')
        #TODO : mettre confirmation a False
        user.confirmation = True
        user.newsletter = True
        user.save()
        user.groups.add(user_group)
        user.save()
        if created:
            permissions_utilisateur = Permission.objects.filter(content_type=ContentType.objects.get(app_label='espace_perso', model='utilisateur').id)
            user_group.permissions.set(permissions_utilisateur)
        return user
    def __init__(self, *args, **kwargs):
        super(FormInscriptionUser, self).__init__(*args, **kwargs)
        self.initial['confirmation'] = 1

    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel']


class FormDataModification(ModelForm):
    
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12'}))
    num_tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12'}))
    
    class Meta:
        model = Personne
        fields = ['nom','prenom','num_tel',]


class FormSelectionQuantite(ModelForm):
    quantite = forms.CharField(initial='1')
    class Meta:
        model = Produit 
        fields = ['quantite']


class FormDataModifProd(ModelForm):
    
    nom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    prenom=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))

    num_tel=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-12 '}))
    image=forms.ImageField(max_length=None,allow_empty_file=".jpg, .jpeg, .png", required=False)
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))

    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def save(self):

        instance = super(FormDataModifProd, self).save(commit=False)
        
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        if x==None or y==None or w==None or h==None :
            x, y, w, h = 0, 0, 100, 100


        image = PILImage.open(instance.image)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((200, 200), PILImage.ANTIALIAS)
        instance.save()
        resized_image.save(instance.image.path)
        return instance

    class Meta:
        model = Producteur
        fields = ['nom', 'prenom','num_tel','description','image','iban', 'x', 'y', 'width', 'height']
    
class FormAide(forms.ModelForm):
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    mail = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    objet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))

    class Meta:
        model = Demandes
        fields = ['nom', 'prenom', 'mail', 'objet','message']
    


class AdresseModifForm(ModelForm):
    adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    ville = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    code_postal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))

    def save(self, commit=True):
        instance = super().save(commit)
        instance.lat, instance.lon = getCoords(instance.adresse, instance.ville, instance.code_postal)
        return instance

    class Meta:
        model = Adresse
        fields = ['code_postal','ville','adresse',]

