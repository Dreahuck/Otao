from django.db import models

class Personne(models.Model):
    username_text = models.CharField(max_length=32, default=" ")
    prenom_text = models.CharField(max_length=32)
    nom_text = models.CharField(max_length=32)
    estActif_bool = models.BooleanField(default=True)
    metier_text = models.CharField(max_length=50)
    pourcentageAttribution_int = models.IntegerField(default=100)
    adresseMail_text = models.CharField(max_length=100, default=" ")
    def __str__(self):
        return self.prenom_text + " " + self.nom_text + "( " + self.metier_text + " )"


class ParametrageTache(models.Model):
	libelleTache_text = models.CharField(max_length=120)
	tempsMoyenTraitementH_dec = models.FloatField(default=0)
	delaisJTolerance = models.IntegerField(default=1)
	def __str__(self):
		return self.libelleTache_text 


class Tache(models.Model):
    tache_text = models.CharField(max_length=120)
    creation_date = models.DateTimeField('Date de création')
    jalon_date = models.DateTimeField('Date Jalon de réalisation')
    commentaire_text = models.CharField(max_length=600)
    priseEnChargePar_id = models.IntegerField(default=999999999)
    creerPar_id =models.IntegerField(default=0)
    urgence_bool = models.BooleanField(default=False)
    codeTache_text = models.CharField(max_length=3)
    etat_text = models.CharField(max_length=2, default="EC")
    def __str__(self):
    	return self.tache_text


class AttestationInfos(models.Model):
    username_text = models.CharField(max_length=32, default=" ")
    prenom = models.CharField(max_length=120)
    nom = models.CharField(max_length=120)
    dateNaissance = models.CharField(max_length=10)
    villeNaissance = models.CharField(max_length=120)
    adressePostal = models.CharField(max_length=120)
    villeActuel = models.CharField(max_length=120)
    def __str__(self):
        return self.prenom + " " + self.nom

