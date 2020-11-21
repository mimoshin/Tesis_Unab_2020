# Generated by Django 3.0.4 on 2020-11-21 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Logistica', '0007_auto_20201121_1831'),
    ]

    operations = [
        migrations.AddField(
            model_name='ind_event',
            name='event_place',
            field=models.CharField(default='event_place', max_length=30),
        ),
        migrations.AddField(
            model_name='ind_event',
            name='event_title',
            field=models.CharField(default='event_title', max_length=40),
        ),
        migrations.AddField(
            model_name='ind_event',
            name='event_type',
            field=models.CharField(default='event_type', max_length=15),
        ),
        migrations.AddField(
            model_name='ind_event',
            name='finish_hour',
            field=models.TimeField(default='09:00 a.m'),
        ),
        migrations.AddField(
            model_name='ind_event',
            name='init_hour',
            field=models.TimeField(default='08:00 a.m'),
        ),
        migrations.AddField(
            model_name='ind_event',
            name='specification',
            field=models.CharField(default='especification', max_length=100),
        ),
    ]