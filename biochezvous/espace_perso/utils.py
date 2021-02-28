from django.core.mail import send_mail
from .models import Utilisateur,Personne,Producteur
from django.http import request
from django.core.mail import EmailMessage

def send_mail_inscription():
    send_mail(
    'Bienvenue sur BioChezVous',
    'Bienvenue' ['nom'],
    'biochezvous.iut@gmail.com',
    ['thomas.laharotte@gmail.com'],
    fail_silently=False,
    )



def mail_mass():
    EmailMessage(
    'Hello',
    'Body goes here',
    'biochezvous.iut@gmail.com',
    [''],
    ['bcc@example.com'],
)