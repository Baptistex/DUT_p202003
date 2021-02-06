from django import forms
from django.forms import ModelForm
from .models import Utilisateur

class ContactFormInscription(ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom','prenom','password','mail','num_tel']

class ProducteurFormInscription(ModelForm):
    class Meta:
        model = Producteur
        fields = ['nom', 'prenom', 'mail', 'num_tel', 'password']

class ProducteurFormConnexion(ModelForm):
    class Meta:
        model = Producteur
        fields = ['nom', 'password']