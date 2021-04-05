from django import forms
from django.forms import Form

class FormAideReponse(forms.Form):
    destinataire = forms.EmailField(label='',widget=forms.TextInput(attrs={'placeholder':'Destinataire'}), required=True)
    objet = forms.CharField(label='',widget=forms.TextInput(attrs={'placeholder':'Objet'}), required=True)
    message = forms.CharField(label='',widget=forms.Textarea(attrs={'placeholder':'Message'}))

    class Meta:
        fields = ['destinataire','objet','message']
