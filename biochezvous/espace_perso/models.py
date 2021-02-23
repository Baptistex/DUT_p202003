from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import Group, Permission, PermissionsMixin, UserManager


class Personne(AbstractBaseUser, PermissionsMixin):
    personne_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100, unique=True)
    num_tel = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10, blank=True)
    ville  = models.CharField(max_length=60, blank=True)
    adresse = models.CharField(max_length = 100,  blank=True)
    panier = models.ManyToManyField('produit.Produit', through='produit.Panier')
    #Pour plus tard :
    #coord_x = models.FloatField()
    #coord_y = models.FloatField()

    USERNAME_FIELD = 'mail'
    objects = UserManager()

    def __str__(self):
        return str(self.personne_id)+str(self.nom)
    
    class Meta:
        db_table = 'personne'


class Utilisateur(Group):
    class Meta:
        proxy = True
        db_table = 'utilisateur'


class Producteur(Group):
    class Meta:
        
        proxy = True
        db_table = 'producteur'


            
        
