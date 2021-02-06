from django import forms
<<<<<<< HEAD
from django.forms import ModelForm
from .models import Utilisateur

class ContactFormInscription(ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom','prenom','mot_de_passe','mail','num_tel']

=======
from .models import Producteur
from django.forms import ModelForm

class ContactFormInscription(forms.Form):
    name = forms.CharField(
        label='Nom',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    lastname = forms.CharField(
        label='Prenom',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True)
    telephone = forms.CharField(
        label='téléphone',
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    motdepasse = forms.CharField(
        label='mot de passe',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )
    verifmdp = forms.CharField(
        label='vérification du mot de passe',
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
        )



class ProducteurFormInscription(ModelForm):
    class Meta:
        model = Producteur
        fields = ['nom', 'prenom', 'mail', 'num_tel', 'password']

class ProducteurFormConnexion(ModelForm):
    class Meta:
        model = Producteur
        fields = ['nom', 'password']
>>>>>>> ac0be71c693cde282b98625599c6ca68a40e9903
