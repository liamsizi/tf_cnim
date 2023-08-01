from django.urls import path
from .import views
urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('logout/',views.logout_user,name="logout"),
    path('login/',views.login_user,name="login"),
    path('commentaire/', views.commentaire, name='commentaire'),
    path('commentaire/<int:commentaire_id>/supprimer/', views.supprimer_commentaire, name='supprimer_commentaire'),

]