from django import forms
from django.forms import ModelForm
from .models import Utilisateur, Personne, Producteur
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group


class FormInscription(UserCreationForm):
    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel']

class FormConnexion(AuthenticationForm):
    class Meta:
        model = Personne
        fields = ['username', 'password']

class FormInscriptionProd(UserCreationForm):
    

    def save(self):
        user = super().save(commit=False)
        prod_group, created = Group.objects.get_or_create(name='producteur')
        user.save()
        user.groups.add(prod_group)
        user.save()
        return user
    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel']




class TestForm(ModelForm):
    class Meta:
        model = Personne
        fields = ['nom','prenom','mail','num_tel'] #Mettre adr ici pour modifier l'adresse

        
