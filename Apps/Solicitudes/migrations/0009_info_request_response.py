# Generated by Django 3.0.4 on 2020-11-10 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Solicitudes', '0008_auto_20201109_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='info_request',
            name='response',
            field=models.CharField(default='response', max_length=400),
        ),
    ]