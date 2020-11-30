# Generated by Django 3.0.4 on 2020-11-30 09:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0001_initial'),
        ('Logistica', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ind_event',
            name='event_place',
        ),
        migrations.RemoveField(
            model_name='ind_event',
            name='event_title',
        ),
        migrations.RemoveField(
            model_name='ind_event',
            name='event_type',
        ),
        migrations.RemoveField(
            model_name='ind_event',
            name='finish_hour',
        ),
        migrations.RemoveField(
            model_name='ind_event',
            name='init_hour',
        ),
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Login.Admin'),
        ),
        migrations.AddField(
            model_name='project',
            name='date_finish',
            field=models.DateField(default='2020-12-12'),
        ),
        migrations.AddField(
            model_name='project',
            name='date_init',
            field=models.DateField(default='2020-12-12'),
        ),
        migrations.AddField(
            model_name='project',
            name='details',
            field=models.CharField(default='2020-12-12', max_length=300),
        ),
        migrations.AddField(
            model_name='project',
            name='project_title',
            field=models.CharField(default='2020-12-12', max_length=60),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(default='2020-12-12', max_length=20),
        ),
        migrations.AlterField(
            model_name='ind_event',
            name='event_date',
            field=models.DateField(default='2020-12-12'),
        ),
    ]
