from .envoyerMail import *
import os
from datetime import datetime, timedelta
from .models import Tache , Personne
import calendar
from .gestionAgenda import *

class NbTacheParPers:
  def __init__(self, nbTacheEnCours, nbTacheTraite, nbTacheAbandon ,nbTacheRefus,prenom_text):
    self.nbTacheEnCours = nbTacheEnCours
    self.nbTacheTraite = nbTacheTraite
    self.nbTacheAbandon = nbTacheAbandon
    self.nbTacheRefus = nbTacheRefus
    self.prenom_text = prenom_text


def rappelTachesEnAttente():
  dateMin = str(datetime.now()) 
  dateMax = str(datetime.now() + timedelta(days=1))
  print('go')
  listeTache = Tache.objects.filter(jalon_date__lte = dateMax)
  #listeTache = Tache.objects.filter(jalon_date__gte = dateMin)
  #listeTache = listeTache.filter(jalon_date__lte = dateMax)
  listeTache = listeTache.filter(etat_text = "EC")
  listeTache = listeTache.order_by('priseEnChargePar_id')
  if not listeTache : 
    return "Aucune tache en attente de traitement"
  html = """\
  <html>
    <head></head>
    <body>
      <p>Bonjour, <br>
         Tu as des taches en attente qui arrive à la date limite ! <br>
         Tu peux les consulter et les éditer <a href="http://192.168.1.81:8000/HomeManager/">ici</a> 
      </p>
    </body>
  </html>
  """


  pecIdEnCours = listeTache[0].priseEnChargePar_id
  listePersonne = [pecIdEnCours]
  for tache in listeTache:
  	if tache.priseEnChargePar_id != pecIdEnCours:
  		pecIdEnCours = tache.priseEnChargePar_id
  		listePersonne.append(pecIdEnCours)

  for personneId in listePersonne:
  	personne = Personne.objects.get(pk=personneId)
  	envoieMailAvecObjet_devAwnTest(personne.adresseMail_text , 'Otao : Tu as des tâches en cours !',' ',html)
  	print("Mail envoyé à : " + personne.adresseMail_text)


def recapTachesDuMois():
  dateDuJour = datetime.today()
  myMonth = dateDuJour.month
  myYear = dateDuJour.year
  lblMois = getMonth(myMonth - 1) + ' ' + str(myYear)
  dateMin = str(dateDuJour.replace(day=1))
  dateMax = str(dateDuJour.replace(day=calendar.monthrange(myYear, myMonth)[1]))
  print('go')
  listeTache = Tache.objects.filter(jalon_date__gte = dateMin)
  listeTache = listeTache.filter(jalon_date__lte = dateMax)
  listeTache = listeTache.order_by('priseEnChargePar_id')
  #listeTacheEnCours = listeTache.filter(etat_text = "EC")
  #listeTacheTraite = listeTache.order_by('priseEnChargePar_id')
  print(listeTache[0])
  personneEnCharge = Personne.objects.get(pk=listeTache[0].priseEnChargePar_id)
  nbTacheEnCours = 0
  nbTacheTraite = 0
  nbTacheAbandon = 0
  nbTacheRefus = 0
  listeDesResultats = []
  for tache in listeTache:
    if personneEnCharge.id == tache.priseEnChargePar_id:
      if tache.etat_text == "EC":
        nbTacheEnCours +=1
      if tache.etat_text == "AB":
        nbTacheAbandon +=1
      if tache.etat_text == "RF":
        nbTacheRefus += 1
      if tache.etat_text == "FN":
        nbTacheTraite += 1
    else :
      nbTacheParPers = NbTacheParPers(nbTacheEnCours , nbTacheTraite , nbTacheAbandon , nbTacheRefus, personneEnCharge.prenom_text)
      listeDesResultats.append(nbTacheParPers)
      personneEnCharge = Personne.objects.get(pk=tache.priseEnChargePar_id)
      nbTacheEnCours = 0
      nbTacheTraite = 0
      nbTacheAbandon = 0
      nbTacheRefus = 0    
      if tache.etat_text == "EC":
        nbTacheEnCours +=1
      if tache.etat_text == "AB":
        nbTacheAbandon +=1
      if tache.etat_text == "RF":
        nbTacheRefus += 1
      if tache.etat_text == "FN":
        nbTacheTraite += 1


  for res in listeDesResultats:
    print("Compte rendu des taches pour " + str(res.prenom_text))
    print("   - Tâches en cours : " + str(res.nbTacheEnCours))
    print("   - Tâches finies : " + str(res.nbTacheTraite))
    print("   - Tâches abandonnées : " + str(res.nbTacheAbandon))
    print("   - Tâches refusées : " + str(res.nbTacheRefus))