# Generated by Django 3.0.4 on 2020-11-19 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0011_athlete_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='other_person',
            name='event',
            field=models.IntegerField(default=0),
        ),
    ]