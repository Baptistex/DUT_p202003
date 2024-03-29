# Generated by Django 3.1.3 on 2021-03-15 18:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('espace_perso', '0008_merge_20210315_1954'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adresse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_postal', models.CharField(blank=True, max_length=10)),
                ('ville', models.CharField(blank=True, max_length=60)),
                ('adresse', models.CharField(blank=True, max_length=100)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('lon', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'adresse',
                'default_permissions': (),
            },
        ),
        migrations.AlterModelOptions(
            name='personne',
            options={'default_permissions': ()},
        ),
        migrations.RemoveField(
            model_name='personne',
            name='code_postal',
        ),
        migrations.RemoveField(
            model_name='personne',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='personne',
            name='lon',
        ),
        migrations.RemoveField(
            model_name='personne',
            name='ville',
        ),
        migrations.RemoveField(
            model_name='personne',
            name='adresse',
        ),
        
    ]
