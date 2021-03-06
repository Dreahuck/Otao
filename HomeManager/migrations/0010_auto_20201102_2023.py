# Generated by Django 3.0.8 on 2020-11-02 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeManager', '0009_attestation'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttestationInfos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prenom', models.CharField(max_length=120)),
                ('nom', models.CharField(max_length=120)),
                ('dateNaissance', models.CharField(max_length=10)),
                ('villeNaissance', models.CharField(max_length=120)),
                ('adressePostal', models.CharField(max_length=120)),
                ('villeActuel', models.CharField(max_length=120)),
            ],
        ),
        migrations.DeleteModel(
            name='Attestation',
        ),
    ]
