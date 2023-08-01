# Generated by Django 4.2.3 on 2023-07-07 08:55

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_commentaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='Societe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('adresse', models.CharField(max_length=100)),
                ('users', models.ManyToManyField(related_name='societes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]