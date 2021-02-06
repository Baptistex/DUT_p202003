from django import forms
from django.forms import ModelForm
from .models import Utilisateur, Producteur
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class ContactFormInscription(ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom','prenom','password','mail','num_tel']

class ProducteurFormInscription(UserCreationForm):
    class Meta:
        model = Producteur
        fields = ['nom', 'prenom', 'mail', 'num_tel']

class ProducteurFormConnexion(AuthenticationForm):
    class Meta:
        model = Producteur
        fields = ['mail', 'password']
