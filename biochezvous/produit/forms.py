from django import forms
from django.forms import ModelForm
from .models import TypeProduit


class TypeProduitForm(ModelForm):
    class Meta:
        model = TypeProduit
        fields = ['nom', 'info', 'prix', 'tva', 'unit', 'image']