# Generated by Django 3.1.3 on 2021-03-27 23:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('espace_perso', '0012_auto_20210322_1418'),
        ('produit', '0008_remove_produit_unite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produit',
            name='producteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='espace_perso.producteur'),
        ),
    ]
