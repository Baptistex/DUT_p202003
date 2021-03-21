from django.db import models

#Classe Demandes pour les pb des utilisateurs
class Demandes(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100, unique=True)
    message = models.CharField(max_length=1500)
    message_id = models.AutoField(primary_key=True)

    class Meta:
        db_table = 'demande'





