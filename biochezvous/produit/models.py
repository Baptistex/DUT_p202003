from django.db import models
from espace_perso.models import Personne

# Create your models here.

class Produit(models.Model):
    produit_id = models.AutoField(primary_key=True)
    producteur = models.ForeignKey('espace_perso.Producteur', on_delete=models.CASCADE)
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
    def __str__(self):
        return self.nom

    def main_image(self):
        return self.images.all().filter(priorite=1).first()

class Image(models.Model):
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='images/')
    priorite = models.IntegerField()  
    
    def delete(self, using=None, keep_parents=False):
        if self.image.storage.exists(self.image.name):
            self.image.storage.delete(self.image.name)
        super().delete()

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
    def __str__(self):
        return self.nom

class Categorie(models.Model):
    categorie_id = models.AutoField(primary_key=True)
    nom = models.TextField()
    typeProduit = models.ForeignKey('TypeProduit', on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'categorie'
        default_permissions = ()
    def __str__(self):
        return self.nom

class Commande(models.Model):

    personne = models.ForeignKey('espace_perso.Personne', related_name='commandes', on_delete=models.CASCADE)
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
