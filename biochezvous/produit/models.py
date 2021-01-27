from django.db import models

# Create your models here.



class TypeProduit(models.Model):
    type_id = models.AutoField(primary_key=True)
    nom = models.TextField()
    info = models.TextField()
    prix = models.FloatField()
    tva = models.FloatField()
    unit = models.BooleanField()
    def __str__(self):
        return "TypeProduit : "+str(type_id)
    
    class Meta:
        db_table = 'typeproduit'


class Produit(models.Model):
    produit_id = models.AutoField(primary_key=True)
    type_id = models.ForeignKey('TypeProduit', on_delete=models.CASCADE)
    date = models.DateField()
    quantite = models.FloatField()
    unite = models.IntegerField()

    def __str__(self):
        return "Produit : "+str(self.produit_id)+str(type_id)
    
    class Meta:
        db_table = 'produit'
