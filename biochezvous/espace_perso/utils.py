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
import requests
import numpy as np

def getCoords(adresse, ville, code_postal):
    """
    Utilise l'API nominatim.openstreetmap.org pour obtenir les coordonées d'une adresse

    Args:
        adresse: numero de rue suivi de la rue
        ville: ville
        code_postal: code postal

    Returns:
        lat: la latitude de l'adresse
        lon: la longitude de l'adresse

    Authors:
        Baptiste Alix
    """
    lat, lon = 0, 0
    url = ('https://nominatim.openstreetmap.org/search?' 
        +'&street='+str(requests.utils.quote(adresse)) 
        +'&city='+str(requests.utils.quote(ville)) 
        +'&country=France'
        +'&postalcode='+str(requests.utils.quote(code_postal)) 
        +'&format=json&addressdetails=0&limit=1')

    response = requests.get(url).json()
    try:
        lat = response[0]['lat']
        lon = response[0]['lon']
    except:
        pass

    return lat, lon



def great_circle_vec(lat1, lng1, lat2, lng2, earth_radius=6_371_009):
    """

    Fonction empruntée de https://github.com/gboeing/osmnx/blob/master/osmnx/distance.py

    Calculate great-circle distances between points.

    Vectorized function to calculate the great-circle distance between two
    points' coordinates or between arrays of points' coordinates using the
    haversine formula. Expects coordinates in decimal degrees.

    Args :
    
        lat1 : float or np.array of float
            first point's latitude coordinate
        lng1 : float or np.array of float
            first point's longitude coordinate
        lat2 : float or np.array of float
            second point's latitude coordinate
        lng2 : float or np.array of float
            second point's longitude coordinate
        earth_radius : int or float
            radius of earth in units in which distance will be returned
            (default is meters)

    Returns :
        dist : float or np.array
            distance or array of distances from (lat1, lng1) to (lat2, lng2) in
            units of earth_radius
    """
    phi1 = np.deg2rad(lat1)
    phi2 = np.deg2rad(lat2)
    d_phi = phi2 - phi1

    theta1 = np.deg2rad(lng1)
    theta2 = np.deg2rad(lng2)
    d_theta = theta2 - theta1

    h = np.sin(d_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(d_theta / 2) ** 2
    h = np.minimum(1.0, h)  # protect against floating point errors

    arc = 2 * np.arcsin(np.sqrt(h))

    # return distance in units of earth_radius
    dist = arc * earth_radius
    return dist
