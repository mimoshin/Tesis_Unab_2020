# Generated by Django 3.0.4 on 2020-11-20 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0013_ievent_organizer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iperson',
            name='first_name',
            field=models.CharField(default='Franco', max_length=40, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='iperson',
            name='last_name',
            field=models.CharField(default='Vega', max_length=40, verbose_name='Apellido'),
        ),
    ]
