from django import forms
from django.forms import ModelForm
from .models import Utilisateur

class ContactFormInscription(ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom','prenom','mot_de_passe','mail','num_tel']

