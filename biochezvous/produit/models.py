from django.db import models
from espace_perso.models import Personne

# Create your models here.

class Produit(models.Model):
    produit_id = models.AutoField(primary_key=True)
    producteur = models.ForeignKey('espace_perso.Personne', on_delete=models.CASCADE)
    categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.FloatField()
    unit = models.BooleanField()
    quantite = models.FloatField()
    unite = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return "Produit : "+str(self.nom)
    
    class Meta:
        db_table = 'produit'


class Image(models.Model):
    produit =models.ForeignKey('Produit', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    
    class Meta:
        db_table = 'image'



class TypeProduit(models.Model):
    type_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    tva = models.FloatField()
    
    class Meta:
        db_table = 'typeproduit'


class Categorie(models.Model):
    categorie_id = models.AutoField(primary_key=True)
    typeProduit = models.ForeignKey('TypeProduit', on_delete=models.CASCADE)
    nom = models.TextField()
        
    def __str__(self):
        return "Categorie : "+str(self.nom)+str(self.categorie_id)

    class Meta:
        db_table = 'categorie'



class Commande(models.Model):

    personne = models.ForeignKey('espace_perso.Personne', on_delete=models.CASCADE)
    commande_id = models.AutoField(primary_key=True)
    date =  models.DateTimeField()
    statut = models.IntegerField() #TODO: à aviser
    montant = models.DecimalField()

    class Meta:
        db_table = 'commande'

class ContenuCommande(models.Model):

    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE)
    quantite = models.IntegerField()

    class Meta:
        db_table = 'contenuCommande'

class Panier(models.Model):
    personne = models.ForeignKey('Personne', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)

    panier_id = models.AutoField(primary_key=True)
    quantite = models.IntegerField()

    class Meta:
        db_table = 'panier'