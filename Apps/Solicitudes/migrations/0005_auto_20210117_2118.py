# Generated by Django 3.0.4 on 2021-01-18 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Solicitudes', '0004_auto_20210117_1309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notify',
            name='object_id',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
