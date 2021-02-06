from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser


class Personne(AbstractBaseUser):
    id_personne = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    num_tel = models.CharField(max_length=100)

    def __str__(self):
        return str(self.person_id)+str(nom)
    
    class Meta:
        db_table = 'personne'
        abstract = True
    
class Utilisateur(Personne):

    class Meta(Personne.Meta):
        db_table = 'utilisateur'

class Producteur(Personne):

    class Meta(Personne.Meta):
        db_table = 'producteur'

