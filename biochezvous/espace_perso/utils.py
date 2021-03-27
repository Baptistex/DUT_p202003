from django.core.mail import send_mail
from .models import Utilisateur,Personne,Producteur
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User



def send_mail_mass():
    list_mail = Personne.objects.filter(groups__name='producteur').values_list('mail', flat=True)
    for mail in list_mail: 
        if Personne.newsletter == True :
            send_mail(
            'Bienvenue sur BioChezVous',
            'Bienvenue',
            'biochezvous.iut@gmail.com',
            [mail],
            fail_silently=False,
    )
        


def send_mail_pay(request):
    mail = request.user.mail
    user = request.user
    mail_subject = 'Votre commande a bien été prise en compte'
    message = render_to_string('pay_email.html', {
            'user': user,
            })
    email = EmailMessage(
            mail_subject, message, to=[mail]
    )
    email.send()
