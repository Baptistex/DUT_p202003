from django.db import models
from espace_perso.models import Personne
# Create your models here.

'''
class Producteur(models.Model):
    personne = models.ForeignKey('espace_perso.Personne', on_delete=models.CASCADE, related_name='personnes')
    description = models.TextField()
    image   = models.ImageField(upload_to='images/')
    #TODO: Champ priorite    
    
    class Meta:
        db_table = 'producteur'
'''
