import logging
from espace_perso.models import Utilisateur,Personne, Producteur
from django.template import Library


register = Library()
logger = logging.getLogger(__name__)


@register.simple_tag( takes_context=True)
def infoConnexion(context):
    request = context['request']
    if(request.user.is_authenticated):
        personne_id = request.user.personne_id
        u = Producteur.objects.filter(personne_ptr_id=personne_id)
        if(u.count()>0):
            typeUser="Producteur"
        else:
            typeUser="Client"
    else:
        typeUser="Inconnu"
    return {'type_user': typeUser}

@register.simple_tag( takes_context=True)
def affDeco(context):
    request = context['request']
    if(request.user.is_authenticated):
        deco=True
    else:
        deco=False
    return {'buttonDeco':deco}

