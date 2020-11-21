# Generated by Django 3.0.4 on 2020-11-19 01:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0004_athlete_athlete_team_iperson_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_title', models.CharField(default='event_title', max_length=40)),
                ('project_type', models.CharField(default='event_type', max_length=15)),
                ('status', models.CharField(default='status', max_length=20)),
                ('specification', models.CharField(default='especification', max_length=100)),
                ('observation', models.CharField(default='observation', max_length=300)),
                ('init_date', models.DateField(default='2020-11-09')),
                ('finish_date', models.DateField(default='2020-11-09')),
            ],
        ),
        migrations.RenameModel(
            old_name='athlete_team',
            new_name='other_person',
        ),
        migrations.RenameField(
            model_name='team_championship',
            old_name='number_teams',
            new_name='max_teams',
        ),
    ]