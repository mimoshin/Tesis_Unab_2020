# Generated by Django 3.0.4 on 2020-11-02 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info_request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='prueba',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('dia', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='request_event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(default='event_title', max_length=40)),
                ('event_type', models.CharField(default='event_type', max_length=15)),
                ('event_place', models.CharField(default='event_place', max_length=30)),
                ('event_date', models.DateField(auto_now=True)),
                ('init_hour', models.TimeField(auto_now=True)),
                ('finish_hour', models.TimeField(auto_now=True)),
                ('specification', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=20)),
                ('observation', models.CharField(max_length=500)),
                ('time_create', models.DateTimeField(auto_now=True)),
                ('petitioner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Login.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Event_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_title', models.CharField(max_length=100)),
                ('event_type', models.CharField(max_length=100)),
                ('event_place', models.CharField(max_length=100)),
                ('event_date', models.CharField(max_length=100)),
                ('init_hour', models.CharField(max_length=100)),
                ('finish_hour', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=20)),
                ('observation', models.CharField(max_length=500)),
                ('time_create', models.DateTimeField(auto_now=True, null=True)),
                ('petitioner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Login.Client')),
            ],
        ),
    ]
