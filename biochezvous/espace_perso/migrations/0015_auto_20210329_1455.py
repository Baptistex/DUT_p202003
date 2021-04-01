# Generated by Django 3.1.3 on 2021-03-29 12:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('espace_perso', '0014_auto_20210328_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adresse',
            name='personne',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='adresse', to=settings.AUTH_USER_MODEL),
        ),
    ]