from django.core.mail import send_mail
from .models import Utilisateur,Personne,Producteur

def send_mail_inscription():
    send_mail(
    'Bienvenue sur BioChezVous',
    'Bienvenue' ['nom'],
    'biochezvous.iut@gmail.com',
    ['mail'],
    fail_silently=False,
    )