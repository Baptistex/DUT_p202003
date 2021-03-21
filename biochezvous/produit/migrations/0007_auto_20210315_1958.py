# Generated by Django 3.1.3 on 2021-03-15 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0006_merge_20210315_1954'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categorie',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='commande',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='contenucommande',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='image',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='panier',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='produit',
            options={'default_permissions': ()},
        ),
        migrations.AlterModelOptions(
            name='typeproduit',
            options={'default_permissions': ()},
        ),
        migrations.RemoveField(
            model_name='panier',
            name='panier_id',
        ),
        migrations.AddField(
            model_name='panier',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
