# views.py
from rest_framework import viewsets

from .serializers import HeroSerializer
from .models import Hero
from HomeManager.models import Personne
from HomeManager.envoiMailRappel import *
from HomeManager.views import *
from HomeManager.AttestationNumerique.main import GenererUneAttestation as generator

from rest_framework.decorators import api_view

class PersonneAttest:
    def __init__(self):
        self.prenom = ""
        self.nom = ""
        self.dateNaissance = ""
        self.villeNaissance = ""
        self.adressePostal = ""
        self.villeActuel = ""
        self.dateSortie = date.today().strftime("%d/%m/%Y")
        self.heureSortie = date.today().strftime("%H:%M")
        self.motif = "sport"



class HeroViewSet(viewsets.ModelViewSet):
    serializer_class = HeroSerializer
    queryset = Hero.objects.all().order_by('name')
    def get_queryset(self):
        retour = Hero.objects.all().order_by('name')
        rappelTachesEnAttente()
        return retour

@api_view(['GET'])
def genererPdf(request, pk):
    print("genererPdf : User :" + request.user)
    utilisateur = Personne.objects.get(username_text= request.user)
    infosAttestation = AttestationInfos.objects.get(username_text = utilisateur.username_text)

    motif = pk
    persAtt = PersonneAttest()
    persAtt.prenom = utilisateur.prenom_text
    persAtt.nom = utilisateur.nom_text
    persAtt.dateNaissance = infosAttestation.dateNaissance
    persAtt.villeNaissance = infosAttestation.villeNaissance
    persAtt.adressePostal = infosAttestation.adressePostal
    persAtt.motif = motif
    persAtt.villeActuel = infosAttestation.villeActuel

    pdfAttest = generator(persAtt)
    img = open(pdfAttest, 'rb')

    response = FileResponse(img)
    return response