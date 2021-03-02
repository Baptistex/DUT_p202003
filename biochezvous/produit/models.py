from django.db import models

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
        

    class Meta:
        db_table = 'categorie'
