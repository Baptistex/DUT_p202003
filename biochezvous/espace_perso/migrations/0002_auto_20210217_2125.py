# Generated by Django 3.1.3 on 2021-02-17 20:25

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from espace_perso.models import Personne
from django.contrib.contenttypes.models import ContentType

def add_group_permissions(apps, schema_editor):

    content_type = ContentType.objects.get_for_model(Personne)
    permission = Permission.objects.create(
        codename='can_view_espace_perso',
        name='Peut voir la page espace perso',
        content_type=content_type
    )
    user_group, created = Group.objects.get_or_create(name='utilisateur')
    prod_group, created = Group.objects.get_or_create(name='producteur')
    #print(prod_group.permissions)


    user_group.permissions.add(
        Permission.objects.get(codename='can_view_espace_perso')
    )

    prod_group.permissions.add(
        Permission.objects.get(codename='can_view_espace_perso')
    )

class Migration(migrations.Migration):

    dependencies = [
        ('espace_perso', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_group_permissions)
    ]
