from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Societe
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()  # Afficher toutes les sociétés dans le formulaire
    Password_societe = forms.CharField(max_length=50, widget=forms.PasswordInput())
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    Password_societe = forms.CharField(max_length=50, widget=forms.PasswordInput())  # Champ pour le mot de passe de la société

