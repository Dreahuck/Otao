# Generated by Django 3.0.8 on 2020-08-01 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomeManager', '0003_auto_20200801_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parametragetache',
            name='tempsMoyenTraitementH_int',
        ),
        migrations.AddField(
            model_name='parametragetache',
            name='tempsMoyenTraitementH_dec',
            field=models.FloatField(default=0),
        ),
    ]