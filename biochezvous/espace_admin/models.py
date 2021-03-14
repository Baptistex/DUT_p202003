from django.db import models

class Demandes(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.CharField(max_length=1500)





