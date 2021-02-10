from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager


class Personne(AbstractBaseUser):
    id_personne = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100, unique=True)
    num_tel = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10, blank=True)
    ville  = models.CharField(max_length=60, blank=True)
    adresse = models.CharField(max_length = 100,  blank=True)
    #Pour plus tard :
    #coord_x = models.FloatField()
    #coord_y = models.FloatField()

    USERNAME_FIELD = 'mail'
    objects = UserManager()

    def __str__(self):
        return str(self.id_personne)+str(self.nom)
    
    class Meta:
        db_table = 'personne'


class Utilisateur(models.Model):
    user = models.OneToOneField(Personne, on_delete=models.CASCADE, primary_key=True)


    class Meta:
        db_table = 'utilisateur'


class Producteur(models.Model):
    user = models.OneToOneField(Personne, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        db_table = 'producteur'

