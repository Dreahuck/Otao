# Generated by Django 3.0.8 on 2020-08-07 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeManager', '0007_personne_adressemail_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='personne',
            name='username_text',
            field=models.CharField(default=' ', max_length=32),
        ),
    ]
