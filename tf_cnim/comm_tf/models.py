from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Projet(models.Model):
    echeance = (
        ('bloque', 'Bloqué'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    )
    nom = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=echeance, default='en_cours')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    def __str__(self):
        return self.nom
class Tache(models.Model) :
    echeance = (
        ('bloque', 'Bloqué'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    )
    nom=models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    status = models.CharField(max_length=50, choices=echeance, default='en_cours')
    projet=models.ForeignKey(Projet,on_delete=models.CASCADE,null=True)
    def __str__(self):
        return self.nom

class Operation(models.Model):
    echeance = (
        ('bloque', 'Bloqué'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    )
    nom=models.CharField(max_length=50)
    crée_par=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,default=1)
    tâche = models.ForeignKey(Tache, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50, choices=echeance, default='en_cours')
    def __str__(self):
        return self.nom
