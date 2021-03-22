from django import forms
from django.forms import ModelForm
from .models import Utilisateur, Personne, Producteur
from produit.models import Image
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Adresse



class FormInscription(UserCreationForm):
    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel']

class FormConnexion(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-2 container-fluid'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-2 container-fluid'}))
    class Meta:
        model = Personne
        fields = ['username', 'password']

class FormInscriptionProd(UserCreationForm):
     
    
    confirmation = forms.BooleanField(widget=forms.HiddenInput(), initial=True) 
    newsletter = forms.BooleanField(widget=forms.HiddenInput(), initial=True) 

    def save(self):
        user = super().save(commit=False)
        prod_group, created = Group.objects.get_or_create(name='producteur')
        user.save()
        user.groups.add(prod_group)
        user.save()

        if created:
            permissions_producteur = Permission.objects.filter(content_type=ContentType.objects.get(app_label='espace_perso', model='producteur').id)
            prod_group.permissions.set(permissions_producteur)
        return user
    class Meta:
        model = Producteur
        fields = ['nom','prenom','mail','num_tel','description','confirmation','newsletter']

class FormInscriptionUser(UserCreationForm):
    
    confirmation = forms.BooleanField(widget=forms.HiddenInput(), initial=True) 
    newsletter = forms.BooleanField(widget=forms.HiddenInput(), initial=True) 

    def save(self):
        user = super().save(commit=False)
        user_group, created = Group.objects.get_or_create(name='utilisateur')
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
        fields = ['nom','prenom','mail','num_tel','confirmation','newsletter']


class FormDataModification(ModelForm):
    
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12 '}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12'}))
    mail = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12'}))
    num_tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12'}))
    #TODO Justine : Créer un nouveau formulaire pour l'adresse
    #adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12'}))
    #ville = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-12'}))
    #code_postal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))

    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel',]
        #'adresse','ville','code_postal',
        
       #widget = { 
            #'nom' : forms.TextInput(attrs={'class': 'form-control'}),
            #'prenom' : forms.TextInput(attrs={'class': 'form-control'}),
            #'mail' : forms.TextInput(attrs={'class': 'form-control'}),
            #'num_tel' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'adresse' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'ville' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'code_postal' : forms.TextInput(attrs={'class': 'form-control'}),
       # }"""

class FormDataModifProd(ModelForm):
    
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    mail = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    num_tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    image=forms.ImageField(max_length=None,allow_empty_file=".jpg, .jpeg, .png", required=False)
    iban = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-3 container-fluid'}))

    class Meta:
        model = Producteur
        fields = ['nom','mail','num_tel','description','image','iban']

        

class AdresseModifForm(ModelForm):
    adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    ville = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    code_postal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-3 container-fluid'}))

    class Meta:
        model = Adresse
        fields = ['code_postal','ville','adresse']