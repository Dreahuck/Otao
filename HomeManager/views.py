from django.http import HttpResponse, JsonResponse, HttpResponseRedirect , FileResponse
from .models import Tache , Personne, ParametrageTache, AttestationInfos
from .envoyerMail import envoieMailNouvelleTache
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.urls import reverse
import json 
from datetime import datetime
from datetime import timedelta
from datetime import date
from django.contrib.auth import authenticate, login as auth_login
import calendar
from .gestionAgenda import *
from .AttestationNumerique.main import GenererUneAttestation as generator

class IndexView(generic.ListView):
	template_name = 'HomeManager/index.html'
	context_object_name = 'dernieres_taches'
	def get_queryset(self):
		taches = Tache.objects.filter(etat_text="EC").order_by('-creation_date')[:25]
		dataJson = []
		for tache in taches:
			if(tache.priseEnChargePar_id > 0):
				personneEnCharge = Personne.objects.get(pk=tache.priseEnChargePar_id)
				tache.PrenomNomEnCharge = personneEnCharge.prenom_text + ' ' + personneEnCharge.nom_text
				tache.UserEnCharge = personneEnCharge.username_text
			else:
				tache.PrenomNomEnCharge = "Non attribué"
				tache.UserEnCharge = " "
			tache.libelleTache = tache.tache_text + ' (' + tache.PrenomNomEnCharge + ')'

			if(tache.creerPar_id > 0):
				personneCreation = Personne.objects.get(pk=tache.creerPar_id)
				tache.PrenomNomCreation = personneCreation.prenom_text + ' ' + personneCreation.nom_text
			else:
				tache.PrenomNomCreation = "Non attribué"

			if (tache.urgence_bool == True):
				urgenceBool = 'true'
			else:
				urgenceBool = 'false'

			groupeAttribution = ParametrageTache.objects.get(pk=tache.codeTache_text)
			tache.GroupeAttributionTache = groupeAttribution.libelleTache_text

			dataJson.append({
			'tache_id': tache.id,
			'tache_text': tache.tache_text,
			'creation_date': tache.creation_date.strftime('%Y-%m-%d'),
			'jalon_date': tache.jalon_date.strftime('%Y-%m-%d'),
			'PrenomNomEnCharge': tache.PrenomNomEnCharge,
			'PrenomNomCreation' : tache.PrenomNomCreation,
			'urgence_bool' : urgenceBool,
			'GroupeAttributionTache': tache.GroupeAttributionTache,
			'UserEnCharge': tache.UserEnCharge
			})
		return dataJson


class DetailTacheView(generic.DetailView):
	model = Tache
	template_name = 'HomeManager/detailTache.html'

def detailPersonne(request, personne_id):
	response = "Détail de la personne %s."
	return HttpResponse(response % personne_id)

def listeTaches(request):
	if request.user.is_authenticated == False:
		print('KO')
		HttpResponseRedirect('/login')
	return HttpResponseRedirect(reverse('HomeManager:index2'))

class CreerUneTacheView(generic.ListView):
	template_name = 'HomeManager/creerUneTache.html'
	context_object_name = 'dataCreerTache'
	def get_queryset(self):
		jsonPersonne = []
		listePersonne = Personne.objects.all()
		for personne in listePersonne:
			if (personne.estActif_bool):
				jsonPersonne.append({
					'prenomEtNom': personne.prenom_text + ' ' + personne.nom_text,
					'id': personne.id
					})
		jsonParametrage = []
		listeParam = ParametrageTache.objects.all()
		for param in listeParam:
			jsonParametrage.append({
				'libelleTache_text' : param.libelleTache_text,
				'id' : param.id
				})
		return {'listePersonne' : jsonPersonne , 'listeParametrage' : jsonParametrage}


def enregistrementAction(request):
	selected_tache_nom = request.POST['txt_tache']
	selected_tache_commentaire = request.POST['txt_commentaire']
	selected_tache_idPersonneEnCharge = request.POST['personne']
	selected_tache_idPersonneOrigine = Personne.objects.get(username_text= request.user).id
	selected_tache_codeParametrage = request.POST['parametrage']
	selected_tache_boolIsUrgent = request.POST.get('isUrgent', False)
	if selected_tache_boolIsUrgent =='on':
		selected_tache_boolIsUrgent =True
	selected_tache_boolIsFuture = request.POST.get('isFuture', False)
	if selected_tache_boolIsFuture =='on':
		dateDeCreation = request.POST.get('dateFuture', datetime.now())
		dateDeCreation = datetime.strptime(dateDeCreation, '%Y-%m-%d')
		print(dateDeCreation)
	else:
		dateDeCreation = datetime.now()

	param = ParametrageTache.objects.get(pk=selected_tache_codeParametrage)
	dateJalonTache = dateDeCreation + timedelta(days=param.delaisJTolerance)
	q = Tache(
		tache_text = selected_tache_nom,
		creation_date = dateDeCreation,
		jalon_date = dateJalonTache,
		commentaire_text = selected_tache_commentaire,
		priseEnChargePar_id = selected_tache_idPersonneEnCharge,
		creerPar_id= selected_tache_idPersonneOrigine,
		urgence_bool = selected_tache_boolIsUrgent,
		codeTache_text = selected_tache_codeParametrage)
	q.save()
	print(selected_tache_idPersonneOrigine)
	print(selected_tache_idPersonneEnCharge)
	print(str(selected_tache_idPersonneOrigine) == str(selected_tache_idPersonneEnCharge))
	if (str(selected_tache_idPersonneOrigine) != str(selected_tache_idPersonneEnCharge)):
		sujet = "[Otao- Nouvelle Tache] : " + selected_tache_nom
		personneEnCharge = Personne.objects.get(pk=selected_tache_idPersonneEnCharge)
		personneOrigine = Personne.objects.get(pk=selected_tache_idPersonneOrigine)
		envoieMailNouvelleTache(personneEnCharge.adresseMail_text,
		 sujet,
		  q.id, 
		  personneOrigine.prenom_text,
		   selected_tache_commentaire)
	return HttpResponseRedirect(reverse('HomeManager:detailTache', args=(q.id,)))


def modificationTache(request, tache_id):
	selected_tache_commentaire = request.POST.get('txt_commentaire')
	selected_tache_etat = request.POST['etatTache']

	q = Tache.objects.get(pk=tache_id)
	q.commentaire_text = selected_tache_commentaire
	if q.etat_text != "":
		q.etat_text = selected_tache_etat
	q.save()

	return HttpResponseRedirect(reverse('HomeManager:index'))



def authentification(request):
	if request.method == 'POST':
		username = Personne.objects.get(adresseMail_text=request.POST['logemail']).username_text
		password = request.POST['logpass']
		print(username)
		user = authenticate(username=username, password=password)
		print(user)
		if user:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect(reverse('HomeManager:index'))
		else:
			error = 'Invalid username or password.'
			return HttpResponseRedirect('/login')




class AgendaView(generic.ListView):
	template_name = 'HomeManager/agenda.html'
	context_object_name = 'moisEnCours'
	def get_queryset(self):
		dateDuJour = datetime.today()
		myMonth = dateDuJour.month
		myYear = dateDuJour.year
		lblMois = getMonth(myMonth - 1) + ' ' + str(myYear)
		dateMin = str(dateDuJour.replace(day=1))
		dateMax = str(dateDuJour.replace(day=calendar.monthrange(myYear, myMonth)[1]))
		listeTache = Tache.objects.filter(jalon_date__gte = dateMin)
		listeTache = listeTache.filter(jalon_date__lte = dateMax)
		listeTache = listeTache.filter(etat_text = "EC")
		monMois = creerAgenda(myYear,myMonth, listeTache)
		return {'htmlMois': monMois, 'titleMois': lblMois}


class AttestationView(generic.ListView):
	template_name = 'HomeManager/attestation.html'
	context_object_name = 'moisEnCours'
	def get_queryset(self):
		return {}


class PersonneAttest:
	def __init__(self):
		self.prenom = ""
		self.nom = ""
		self.dateNaissance = ""
		self.villeNaissance = "Dechy"
		self.adressePostal = ""
		self.villeActuel = ""
		self.dateSortie = date.today().strftime("%d/%m/%Y")
		self.heureSortie = date.today().strftime("%H:%M")
		self.motif = "sport"

def GenererUneAttestation(request):
	print(request.user)
	utilisateur = Personne.objects.get(username_text= request.user)
	infosAttestation = AttestationInfos.objects.get(username_text = utilisateur.username_text)

	motif = request.POST['lblMotif']
	persAtt = PersonneAttest()
	persAtt.prenom = utilisateur.prenom_text
	persAtt.nom = utilisateur.nom_text
	persAtt.dateNaissance = infosAttestation.dateNaissance
	persAtt.villeNaissance = infosAttestation.villeNaissance
	persAtt.adressePostal = infosAttestation.adressePostal
	persAtt.motif = motif
	persAtt.villeActuel = infosAttestation.villeActuel

	pdfAttest = generator(persAtt)
	print(pdfAttest)

	img = open(pdfAttest, 'rb')

	response = FileResponse(img)
	return response
