from django.urls import path
from .import views
urlpatterns = [
    path('',views.home,name="home"),
    path('acceuilprojet/',views.acceuilprojet,name="acceuilprojet"),
    path('afficherprojet/',views.afficherProjet,name="afficherProjet"),
    path('ajouterprojet/',views.projetForm,name="ajouterProjet"),
    path('projets/detailProjet/<str:pk>/',views.detailProjet,name="detailProjet"),
    path('projets/update/<str:pk>/',views.updateProjet,name="updateProjet"),
    path('projets/delete/<str:pk>/',views.deleteProjet,name="deleteProjet"),
    path('projet/<int:projet_id>/update_status/', views.update_status, name='update_status'),


    path('acceuil/',views.acceuil,name="acceuil"),
    path('afficher/',views.afficherTache,name="afficherTache"),
    path('ajouter/',views.tacheForm,name="ajouterTache"),
    path('rechercher/',views.recherche,name="rechercher"),
    path('taches/detailTache/<str:pk>/',views.detailTache,name="detailTache"),
    path('taches/update/<str:pk>/',views.updateTache,name="updateTache"),
    path('taches/delete/<str:pk>/',views.deleteTache,name="deleteTache"),

    path('tache/<int:tache_id>/update_tache_status/', views.update_tache_status, name='update_tache_status'),

    path('afficherOperation/',views.afficherOperation,name="afficherOperation"),
    path('ajouterOperation/',views.operationForm,name="ajouterOperation"),
    path('operations/update/<str:pk>/',views.updateOperation,name="updateOperation"),
    path('operation/delete/<str:pk>/',views.deleteOperation,name="deleteOperation"),

    path('operation/<int:operation_id>/update_op_status/', views.update_op_status, name='update_op_status'),
    path('tache/<int:tache_id>/update_projet_status/', views.update_projet_status, name='update_projet_status'),
]