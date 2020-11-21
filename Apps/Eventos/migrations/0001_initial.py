# Generated by Django 3.0.4 on 2020-11-17 23:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='iEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(default='event_title', max_length=40)),
                ('event_type', models.CharField(default='event_title', max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Team_championship',
            fields=[
                ('ievent_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Eventos.iEvent')),
                ('number_teams', models.CharField(default='event_title', max_length=40)),
            ],
            bases=('Eventos.ievent',),
        ),
    ]
