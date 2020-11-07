from django.urls import include, path

from . import views
from django.contrib.auth import views as auth_views


app_name = 'HomeManager'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:personne_id>/', views.listeTaches, name='listeTaches'),
    path('<int:personne_id>/detailPersonne', views.detailPersonne, name='detailPersonne'),
    path('detailTache/<int:pk>', views.DetailTacheView.as_view(), name='detailTache'),
    path('creerUneTache', views.CreerUneTacheView.as_view(), name='creerUneTache'),
    path('enregistrementAction/', views.enregistrementAction, name='enregistrementAction'),
    path('<int:tache_id>/modificationTache/', views.modificationTache, name='modificationTache'),
    path('authentification', views.authentification, name='authentification'),
    path('agenda', views.AgendaView.as_view(), name='agenda'),
    path('attestation', views.AttestationView.as_view(), name='attestation'),
    path('GenererUneAttestation/', views.GenererUneAttestation, name='GenererUneAttestation'),
]