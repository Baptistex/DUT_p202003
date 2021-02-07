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
