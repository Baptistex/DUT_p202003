from django import forms
from django.forms import ModelForm
from .models import Utilisateur, Personne
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class FormInscription(UserCreationForm):
    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel']

class FormConnexion(AuthenticationForm):
    class Meta:
        model = Personne
        fields = ['username', 'password']

class FormDataModification(ModelForm):
    
    nom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))
    prenom = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))
    mail = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))
    num_tel = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))
    adresse = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))
    ville = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6'}))
    code_postal = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-3'}))

    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel','adresse','ville','code_postal',]

       #widget = { 
            #'nom' : forms.TextInput(attrs={'class': 'form-control'}),
            #'prenom' : forms.TextInput(attrs={'class': 'form-control'}),
            #'mail' : forms.TextInput(attrs={'class': 'form-control'}),
            #'num_tel' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'adresse' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'ville' : forms.TextInput(attrs={'class': 'form-control'}),
           # 'code_postal' : forms.TextInput(attrs={'class': 'form-control'}),
       # }"""

        
