from django.core.mail import send_mail
from .models import Utilisateur,Personne,Producteur
from django.core.mail import EmailMessage

def send_mail_ins(request):

    mail = request.user.mail
    send_mail(
    'Bienvenue sur BioChezVous',
    'Bienvenue',
    'biochezvous.iut@gmail.com',
    [mail],
    fail_silently=False,
    )



def send_mail_mass():
    list_mail = Personne.objects.filter(groups__name='producteur').values_list('mail', flat=True)
    for mail in list_mail: 
        send_mail(
        'Bienvenue sur BioChezVous',
        'Bienvenue',
        'biochezvous.iut@gmail.com',
        [mail],
        fail_silently=False,
    )


def send_mail_pay(request):

    mail = request.user.mail
    send_mail(
    'Votre commande à été validé',
    'Bienvenue',
    'biochezvous.iut@gmail.com',
    [mail],
    fail_silently=False,
    )