from django.db import models

# Create your models here.



class TypeProduit(models.Model):
    type_id = models.AutoField(primary_key=True)
    #Pour plus tard, quand le modele sera utilisable avec des sessions
    #producteur_id = models.ForeignKey('Producteur', on_delete=models.CASCADE)
    nom = models.TextField()
    info = models.TextField()
    prix = models.FloatField()
    tva = models.FloatField()
    unit = models.BooleanField()
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return "TypeProduit : "+str(type_id)
    
    class Meta:
        db_table = 'typeproduit'


class Produit(models.Model):
    produit_id = models.AutoField(primary_key=True)
    type_id = models.ForeignKey('TypeProduit', on_delete=models.CASCADE)
    cat_id = models.ForeignKey('CategorieProduits', on_delete=models.CASCADE)
    date = models.DateField()
    quantite = models.FloatField()
    unite = models.IntegerField()

    def __str__(self):
        return "Produit : "+str(self.produit_id)+str(type_id)
    
    class Meta:
        db_table = 'produit'


class CategorieProduits(models.Model):
    cat_nom = models.TextField()
    cat_id = models.AutoField(primary_key=True)


    class Meta:
        db_table = 'CategorieProduits'
        
    def __str__(self):
        return "Categorie : "+str(self.produit_id)+str(type_id)
