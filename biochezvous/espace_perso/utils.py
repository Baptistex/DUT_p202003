import requests


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
    lat = response[0]['lat']
    lon = response[0]['lon']

    return lat, lon