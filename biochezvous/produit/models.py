from django.db import models

# Create your models here.



class Produit(models.Model):
    id_produit = models.AutoField(primary_key=True)
    id_producteur = models.ForeignKey('espace_perso.Producteur', on_delete=models.CASCADE)
    id_categorie = models.ForeignKey('Categorie', on_delete=models.CASCADE)
    nom = models.CharField(max_length=50)
    description = models.TextField()
    prix = models.FloatField()
    unit = models.BooleanField()
    quantite = models.FloatField()
    unite = models.IntegerField()
    date = models.DateTimeField()

    def __str__(self):
        return "Produit : "+str(nom)
    
    class Meta:
        db_table = 'produit'


class Image(models.Model):
    id_produit =models.ForeignKey('Produit', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return "Image : "+str(image)
    
    class Meta:
        db_table = 'image'



class TypeProduit(models.Model):
    id_type = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=50)
    tva = models.FloatField()

    def __str__(self):
        return "Produit : "+str(nom)+str(id_type)
    
    class Meta:
        db_table = 'typeproduit'


class Categorie(models.Model):
    id_categorie = models.AutoField(primary_key=True)
    id_type = models.ForeignKey('TypeProduit', on_delete=models.CASCADE)
    nom = models.TextField()
        
    def __str__(self):
        return "Categorie : "+str(nom)+str(id_categorie)

    class Meta:
        db_table = 'categorie'
