from django import forms

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