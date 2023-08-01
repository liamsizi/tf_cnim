from django.contrib.auth import get_user_model
from.models import Tache,Operation,Projet
from .form import TacheForm,OperationForm,ProjetForm
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.urls import reverse
User=get_user_model()
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Operateur
def home(request):
    return render (request,'home.html')
@login_required
def acceuilprojet(request):
    return render(request,'acceuilprojet.html')

@login_required
def acceuil(request):
    current_date = datetime.today() # Get the current date in the desired format
    context = {
        'current_date': current_date,
    }
    return render(request, 'acceuil.html', context)

@login_required
def afficherProjet(request):
    current_date = datetime.today()  # Get the current date in the desired format
    context = {
        'current_date': current_date,
    }
    projets=Projet.objects.all()
    return render(request,'list_projet.html',{'projets':projets,'current_date': current_date})

def afficherTache(request):
    taches=Tache.objects.all()
    return render(request,'detailProjet.html',{'taches':taches})

def afficherOperation(request):
    operations=Operation.objects.all()
    return render(request,'detailTache.html',{'operations':operations})


def projetForm(request):
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user  # Set the created_by field to the current user
            form.save()
            return redirect('afficherProjet')
        else:
            print(form.errors)  # Add this line to check for form validation errors
    else:
        form = ProjetForm()

    return render(request, 'ajouterProjet.html', {'form': form})

def tacheForm(request):
    projet_id = request.GET.get('projet_id')
    if projet_id:
        try:
            projet = Projet.objects.get(pk=projet_id)
        except Projet.DoesNotExist:
            # Handle the case when the specified projet_id doesn't exist
            # Redirect or show an error message as needed
            pass
        else:
            if request.method == 'POST':
                form = TacheForm(request.POST)
                if form.is_valid():
                    tache = form.save(commit=False)
                    tache.projet = projet

                    # Set the creator as the current user
                    tache.created_by = request.user

                    tache.save()

                    url = reverse('detailProjet', kwargs={'pk': projet_id})
                    return redirect(url)
            else:
                form = TacheForm()
    else:
        # Handle the case when no projet_id is provided in the URL or other source
        # Redirect or show an error message as needed
        pass

    return render(request, 'ajouterTache.html', {'form': form})


def operationForm(request):
    tache_id = request.GET.get('tache_id')
    if tache_id:
        try:
            tache = Tache.objects.get(pk=tache_id)
        except Tache.DoesNotExist:
            # Handle the case when the specified tache_id doesn't exist
            # Redirect or show an error message as needed
            pass
        else:
            if request.method == 'POST':
                form = OperationForm(request.POST)
                if form.is_valid():
                    operation = form.save(commit=False)
                    operation.tâche = tache

                    # Set the creator as the current user
                    operation.crée_par = request.user

                    operation.save()

                    url = reverse('detailTache', kwargs={'pk': tache_id})
                    return redirect(url)
            else:
                form = OperationForm()
    else:
        # Handle the case when no tache_id is provided in the URL or other source
        # Redirect or show an error message as needed
        pass

    return render(request, 'ajouterOperation.html', {'form': form})

def recherche(request):
    if request.method=="POST":
        search=request.POST['search']
        taches=Tache.objects.filter(nom__icontains=search)
        return render(request,'rechercher.html',{'taches':taches,'search':search})

def detailProjet(request, pk):
    projet = Projet.objects.get(id=pk)  # Retrieve associated tasks
    taches = projet.tache_set.all()
    return render(request, 'detailProjet.html', {'projet': projet,'taches': taches})
def detailTache(request, pk):
    tache = Tache.objects.get(id=pk)  # Retrieve associated operations
    operations = tache.operation_set.all()
    return render(request, 'detailTache.html', {'tache': tache,'operations': operations})

def updateProjet(request,pk):
    projets=Projet.objects.get(id=pk)
    form=ProjetForm(instance=projets)
    if request.method=="POST":
        form=ProjetForm(request.POST,instance=projets)
        if form.is_valid():
            form.save()
            return redirect('afficherProjet')
    context={'form':form}
    return render(request,'projetForm.html',context)
def updateTache(request,pk):
    taches=Tache.objects.get(id=pk)
    form=TacheForm(instance=taches)
    if request.method=="POST":
        form=TacheForm(request.POST,instance=taches)
        if form.is_valid():
            form.save()
            url = reverse('detailProjet', kwargs={'pk': taches.projet.pk})
            return redirect(url)
    context={'form':form}
    return render(request,'TacheForm.html',context)

def updateOperation(request,pk):
    operations=Operation.objects.get(id=pk)
    form=OperationForm(instance=operations)
    if request.method=="POST":
        form=OperationForm(request.POST,instance=operations)
        if form.is_valid():
            form.save()
            url = reverse('detailTache', kwargs={'pk': operations.tâche.pk})
            return redirect(url)
    context={'form':form}
    return render(request,'operationForm.html',context)

def deleteProjet(request,pk):
    projet=Projet.objects.get(id=pk)
    if request.method=="POST":
        projet.delete()
        return redirect ('afficherProjet')
    context={'item':projet}
    return render(request,'deleteProjet.html',context)

def deleteTache(request,pk):
    tache=Tache.objects.get(id=pk)
    if request.method=="POST":
        tache.delete()
        url = reverse('detailProjet', kwargs={'pk': tache.projet.pk})
        return redirect(url)
    context={'item':tache}
    return render(request,'deleteTache.html',context)

def deleteOperation(request,pk):
    operation=Operation.objects.get(id=pk)
    if request.method=="POST":
        operation.delete()
        url = reverse('detailTache', kwargs={'pk': operation.tâche.pk})
        return redirect(url)
    context={'item':operation}
    return render(request,'deleteOperation.html',context)

def update_status(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        projet.status = status
        projet.save()
        return redirect('afficherProjet')

    return render(request, 'update_status.html', {'projet': projet})

def update_tache_status(request, tache_id):
    tache = get_object_or_404(Tache, id=tache_id)

    if request.method == 'POST':
        status = request.POST.get('status')
        tache.status = status
        tache.save()
        url = reverse('detailProjet', kwargs={'pk': tache.projet.pk})
        #send_tache_status_notification(tache)
        return redirect(url)

    return render(request, 'update_status.html', {'tache': tache})

def update_op_status(request, operation_id):
    operation = get_object_or_404(Operation, id=operation_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        operation.status = status
        operation.save()

        # Update the tache status
        tache = operation.tâche
        any_operation_bloque = tache.operation_set.filter(status='bloque').exists()
        all_operations_termine = tache.operation_set.filter(status='termine').count() == tache.operation_set.count()

        if any_operation_bloque:
            tache.status = 'bloque'
            send_tache_bloquee_notification(tache, operation)
        elif all_operations_termine:
            tache.status = 'termine'
            send_tache_terminee_notification(tache)
        else:
            tache.status = 'en_cours'

        tache.save()

        # Redirect to the detailTache view for the tache associated with this operation
        url = reverse('detailTache', kwargs={'pk': tache.pk})
        return redirect(url)

    return render(request, 'update_status.html', {'operation': operation})



@receiver(post_save, sender=Tache)
def update_projet_status(sender, instance, **kwargs):
    projet = instance.projet
    if projet:
        any_tache_bloque = projet.tache_set.filter(status='bloque').exists()
        all_taches_termine = projet.tache_set.filter(status='termine').count() == projet.tache_set.count()

        if any_tache_bloque:
            projet.status = 'bloque'
            send_projet_bloquee_notification(projet)
        elif all_taches_termine:
            projet.status = 'termine'
            send_projet_termine_notification(projet)  # Call the email notification function for project status change
        else:
            projet.status = 'en_cours'

        projet.save()


def send_tache_terminee_notification(tache):
    subject = f"Notification : Tâche '{tache.nom}' liée au projet '{tache.projet.nom}' est terminée"
    message = f"La tâche '{tache.nom}' a été marquée comme terminée. Félicitations pour la réalisation de toutes les opérations liées à cette tâche."
    from_email = 'your_email@example.com'
    recipient_list = []

    # Get other users who are not the task creator
    autres_utilisateurs = Operateur.objects.exclude(id=tache.created_by.id)
    for utilisateur in autres_utilisateurs:
        recipient_list.append(utilisateur.email)

    send_mail(subject, message, from_email, recipient_list)

def send_projet_termine_notification(projet):
    subject = f"Notification : Projet '{projet.nom}' terminé"
    message = f"Le projet '{projet.nom}' a été marqué comme terminé. Félicitations pour la réalisation de toutes les tâches liées à ce projet."
    from_email = 'your_email@example.com'
    recipient_list = []

    # Get other users who are not the project creator
    autres_utilisateurs = Operateur.objects.exclude(id=projet.created_by.id)
    for utilisateur in autres_utilisateurs:
        recipient_list.append(utilisateur.email)

    send_mail(subject, message, from_email, recipient_list)

def send_tache_bloquee_notification(tache,operation):
    subject = f"Notification : Tâche '{tache.nom}' liée au projet '{tache.projet.nom}' est bloquée"
    message = f"La tâche '{tache.nom}' est bloquée à cause du blocage de l'opération '{operation.nom}'."
    from_email = 'your_email@example.com'
    recipient_list = []
    autres_utilisateurs = Operateur.objects.exclude(id=tache.created_by.id)
    for utilisateur in autres_utilisateurs:
        recipient_list.append(utilisateur.email)

    send_mail(subject, message, from_email, recipient_list)

def send_projet_bloquee_notification(projet):
    subject = f"Notification : Projet '{projet.nom}' bloqué"
    message = f"Le projet '{projet.nom}' est bloqué,indiquee par {projet.created_by.email}"
    from_email = 'your_email@example.com'
    recipient_list = []
    autres_utilisateurs = Operateur.objects.exclude(id=projet.created_by.id)
    for utilisateur in autres_utilisateurs:
        recipient_list.append(utilisateur.email)

    send_mail(subject, message, from_email, recipient_list)
