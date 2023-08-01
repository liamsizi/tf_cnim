from django import forms
from .models import Tache,Operation,Projet
from accounts.models import Operateur
class ProjetForm(forms.ModelForm):
    class Meta:
        model = Projet
        fields = "__all__"
        exclude = ['created_by']
class TacheForm(forms.ModelForm):
    class Meta:
        model=Tache
        fields="__all__"
        exclude = ['projet', 'created_by',]
class OperationForm(forms.ModelForm):
    class Meta :
        model=Operation
        fields = "__all__"
        exclude = ['tâche', 'crée_par']
