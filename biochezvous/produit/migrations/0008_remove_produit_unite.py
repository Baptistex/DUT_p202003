# Generated by Django 3.1.3 on 2021-03-15 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produit', '0007_auto_20210315_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produit',
            name='unite',
        ),
    ]
