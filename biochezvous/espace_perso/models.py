from django.db import models


class Personne(models.Model):

    person_id = models.AutoField(primary_key=True)
    nom = models.TextField()
    prenom = models.TextField()
    mot_de_passe = models.TextField()
    mail = models.TextField()
    num_tel = models.TextField()


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