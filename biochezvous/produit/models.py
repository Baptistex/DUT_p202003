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
    unit = models.CharField(max_length=10)
    quantite = models.FloatField()
    date = models.DateTimeField()

    
    class Meta:
        db_table = 'produit'
        default_permissions = ()

class Image(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    image   = models.ImageField(upload_to='images/')
    priorite = models.IntegerField()  
    
    class Meta:
        db_table = 'image'
        default_permissions = ()



class TypeProduit(models.Model):
    type_id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    tva = models.FloatField()

    
    class Meta:
        db_table = 'typeproduit'
        default_permissions = ()

class Categorie(models.Model):
    categorie_id = models.AutoField(primary_key=True)
    typeProduit = models.ForeignKey('TypeProduit', on_delete=models.CASCADE)
    nom = models.TextField()
        

    class Meta:
        db_table = 'categorie'
        default_permissions = ()


class Commande(models.Model):

    personne = models.ForeignKey('espace_perso.Personne', on_delete=models.CASCADE)
    commande_id = models.AutoField(primary_key=True)
    date =  models.DateTimeField()
    statut = models.IntegerField() #TODO: à aviser
    montant = models.DecimalField(max_digits=8, decimal_places=3)
    produits = models.ManyToManyField('produit.Produit', through='produit.ContenuCommande')


    class Meta:
        db_table = 'commande'
        default_permissions = ()

class ContenuCommande(models.Model):

    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE)
    quantite = models.IntegerField()

    class Meta:
        db_table = 'contenuCommande'
        default_permissions = ()

class Panier(models.Model):
    personne = models.ForeignKey('espace_perso.Personne', related_name='panier_personne', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    quantite = models.IntegerField()

    class Meta:
        db_table = 'panier'
        default_permissions = ()
