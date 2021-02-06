from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser

<<<<<<< HEAD

class Personne(models.Model):
    id_personne = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    num_tel = models.CharField(max_length=100)
=======
class Personne(AbstractBaseUser):
    id_personne = models.AutoField(primary_key=True)
    nom = models.TextField()
    prenom = models.TextField()
    mail = models.TextField()
    num_tel = models.TextField()
>>>>>>> ac0be71c693cde282b98625599c6ca68a40e9903

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

