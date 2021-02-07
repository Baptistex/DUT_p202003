# Generated by Django 3.1.3 on 2021-02-07 01:32

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Personne',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id_personne', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('mail', models.EmailField(max_length=100, unique=True)),
                ('num_tel', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'personne',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Producteur',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='espace_perso.personne')),
            ],
            options={
                'db_table': 'producteur',
            },
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='espace_perso.personne')),
            ],
            options={
                'db_table': 'utilisateur',
            },
        ),
    ]
