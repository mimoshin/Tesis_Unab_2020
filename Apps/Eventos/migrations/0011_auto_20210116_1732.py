# Generated by Django 3.0.4 on 2021-01-16 20:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Eventos', '0010_auto_20210116_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athlete_team',
            name='my_team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Eventos.Team'),
        ),
    ]