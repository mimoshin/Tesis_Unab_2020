# Generated by Django 3.1.7 on 2021-04-30 02:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('Solicitudes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Viewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(default=1)),
                ('name', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=False)),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'Solicitudes'), ('model', 'event_request')), models.Q(('app_label', 'Solicitudes'), ('model', 'info_request')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Notify',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField(default=1)),
                ('view', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'Solicitudes'), ('model', 'event_request')), models.Q(('app_label', 'Solicitudes'), ('model', 'info_request')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]