# Generated by Django 4.2.3 on 2023-07-20 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comm_tf', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operation',
            name='case',
        ),
        migrations.RemoveField(
            model_name='tache',
            name='is_case',
        ),
    ]
