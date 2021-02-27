from django.core.mail import send_mail
from .models import Utilisateur,Personne,Producteur
from django.http import request

def send_mail_inscription():
    if(request.GET.get('pay')):
        send_mail(
        'Bienvenue sur BioChezVous',
        'Bienvenue' ['nom'],
        'biochezvous.iut@gmail.com',
        ['thomas.laharotte@gmail.com'],
        fail_silently=False,
        )