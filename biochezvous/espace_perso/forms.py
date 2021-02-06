from django import forms
from django.forms import ModelForm
from .models import Utilisateur

class ContactFormInscription(ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom','prenom','password','mail','num_tel']

