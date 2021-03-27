from django import forms
from django.forms import Form

class FormAideReponse(forms.Form):
    destinataire = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    objet = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-6 container-fluid'}))

    class Meta:
        fields = ['destinataire','objet','message']
