from django.contrib.auth.models import AbstractUser,User
from django.db import models
from django.conf import settings

class Operateur(AbstractUser):
    pass

class Commentaire(models.Model):
    utilisateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commentaire de {self.utilisateur.username}"


class Societe(models.Model):
    nom = models.CharField(max_length=100)
    Password_societe = models.CharField(max_length=50,default='0000')  # Ajoutez un champ pour le mot de passe de la société

    def __str__(self):
        return self.nom

