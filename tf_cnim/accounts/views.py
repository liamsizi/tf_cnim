from django.contrib.auth import get_user_model,login,logout,authenticate
from django.shortcuts import render,redirect,get_object_or_404
from .models import Commentaire,Societe
from django.core.mail import send_mail
from django.contrib import messages
from .form import LoginForm
from django.contrib.auth.decorators import login_required

User=get_user_model()

def signup(request):
    if request.method == 'POST':
        # Traitement du formulaire d'inscription
        # Récupération des données du formulaire
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        Password_societe = request.POST.get('Password_societe','')
        # Autres champs du formulaire...

        # Vérifiez si le code saisi correspond à l'un des codes spécifiques enregistrés
        try:
            societe = Societe.objects.get(Password_societe=Password_societe)
        except Societe.DoesNotExist:
            return render(request, 'invalid_code.html')

        # Créez un nouvel utilisateur avec les données du formulaire
        user = User.objects.create_user(username=username, password=password,email=email)
        # Effectuez d'autres opérations nécessaires, par exemple, enregistrer des informations supplémentaires sur l'utilisateur

        # Redirigez l'utilisateur vers la page d'accueil
        return redirect('afficherProjet')  # Remplacez 'accueil' par le nom de l'URL de votre page d'accueil
    else:
        # Afficher le formulaire d'inscription vide
        return render(request, 'signup.html')

def logout_user(request):
    logout(request)
    return redirect('home')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            Password_societe = form.cleaned_data['Password_societe']

            try:
                societe = Societe.objects.get(Password_societe=Password_societe)
            except Societe.DoesNotExist:
                return render(request, 'invalid_code.html')
            else:
                user = authenticate(request, username=username, password=password, Password_societe=Password_societe)
                if user is not None:
                    login(request, user)
                    return redirect('afficherProjet')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

@login_required
def commentaire(request):
    commentaires = Commentaire.objects.all()

    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        commentaire = Commentaire(utilisateur=request.user, contenu=contenu)
        commentaire.save()
        return redirect('commentaire')  # Rediriger vers la page des commentaires après soumission

    return render(request, 'commentaire.html', {'commentaires': commentaires})

def supprimer_commentaire(request, commentaire_id):
    commentaire = get_object_or_404(Commentaire, id=commentaire_id)

    # Check if the user is the owner of the comment
    if commentaire.utilisateur == request.user:
        commentaire.delete()

    return redirect('commentaire')












