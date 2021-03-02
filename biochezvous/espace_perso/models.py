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
    #Pour plus tard :
    #coord_x = models.FloatField()
    #coord_y = models.FloatField()

    USERNAME_FIELD = 'mail'
    objects = UserManager()

    
    class Meta:
        db_table = 'personne'
        

class Utilisateur(Personne):

    class Meta:
        db_table = 'utilisateur'
        permissions = [
            ('can_view_espace_perso', 'Peux acceder a la page espace perso'),
        ]

class Producteur(Personne):
    description = models.TextField()
    image   = models.ImageField(upload_to='images/')
    class Meta:
        db_table = 'producteur'
        default_permissions = ()
        permissions = [
            ('can_view_espace_perso', 'Peux acceder a la page espace perso'),
            ('can_view_espace_producteur', 'Peux acceder a la page espace producteur'),
        ]


