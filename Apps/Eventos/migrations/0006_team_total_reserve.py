# Generated by Django 3.0.4 on 2020-11-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0005_athlete_team_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='total_reserve',
            field=models.IntegerField(default=0),
        ),
    ]
