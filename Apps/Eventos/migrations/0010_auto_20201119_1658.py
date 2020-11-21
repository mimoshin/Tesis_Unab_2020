# Generated by Django 3.0.4 on 2020-11-19 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0009_auto_20201119_1657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='athlete',
            name='status',
        ),
        migrations.AddField(
            model_name='athlete',
            name='event',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='iperson',
            name='status',
            field=models.CharField(default='noActive', max_length=40),
        ),
    ]