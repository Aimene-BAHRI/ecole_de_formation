# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from distutils.command.upload import upload
from email.headerregistry import Address
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import OneToOneField
from django.utils import timezone

from django.urls import reverse
# Create your models here.
from datetime import date, datetime
monthy = datetime.today().month
yearly = datetime.today().year

class Parent(models.Model):
	Plan_CHOICES = (
		("mentuelle", "Mentuelle"),
		("trimestrielle", "Trimestrielle"),
		("6_mois", "6 Mois"),
		("annuelle", "Annuelle"),
	)
	user = models.OneToOneField(User, verbose_name="utilisateur", on_delete=models.CASCADE, related_name="parant")
	father_name = models.CharField("nom du père", max_length=100)
	father_profession = models.CharField("profession du père", max_length=300)
	father_phone = models.CharField("numéro de téléphone du père", max_length=20)
	father_avatar = models.ImageField(upload_to = 'avatars/')
	mother_name = models.CharField("nom et prénom de la mère", max_length=100)
	mother_profession = models.CharField("profession de la mère", max_length=300)
	mother_phone = models.CharField("numéro de téléphone de la mère", max_length=20)
	authorized_people = models.TextField("personnes autorisées à recuperer l'eleve")
	subscribed_plan = models.CharField("le plan d'abonement", choices=Plan_CHOICES, max_length=30, default="mentuelle")

	def __str__(self):
		return '{} __ {}'.format(self.user, self.father_name)

	def get_total_paied(self):
		factures = Abonement.objects.filter(operateur = self)
		total = 0
		for facture in factures:
			total = total + facture.balance()
		return total

	def get_total_a_payer(self):
		factures = Facture.objects.filter(operateur = self.user)
		total = 0
		for facture in factures:
			total = total + facture.reste_a_paier
		return total

	def get_fils_count(self):
		fils = self.fils.all().count()
		return fils

class StudyLevel(models.Model):
	Year_CHOICES = (
		("1ere année", "1ere année"),
		("2eme année", "2eme année"),
		("3eme année", "3eme année"),
		("4eme année", "4eme année"),
		("5eme année", "5eme année"),
		("6eme année", "6eme année"),
	)
	NIVEAU_CHOICES = (
		("prescolaire", "Prescolaire"),
		("preparatoire", "Preparatoire"),
		("primaire", "Primaire"),
		("moyenne", "Moyenne"),
		("lycéenne", "Lycéenne"),
	)
	Classe_CHOICES = (
		("classe 1", "Classe 1"),
		("classe 2", "Classe 2"),
		("classe 3", "Classe 3"),
		("classe 4", "Classe 4"),
		("classe 5", "Classe 5"),
	)
	DEVISION_CHOICES = (
		("Tronc_commun_science_et_technologie" , "Tronc commun science et technologie"),
		("sciences expérimentales" , "sciences expérimentales"),
		("Mathématiques" , "Mathématiques"),
		("Athlète technique" , "Athlète technique")
	)
	year = models.CharField("l'année scolaire",max_length=20, choices=Year_CHOICES, default="1ere année")
	level = models.CharField("niveau d'etude scolaire",max_length=20, choices=NIVEAU_CHOICES, default="prescolaire")
	classe = models.CharField("classe scolaire",max_length=20, choices=Classe_CHOICES, null=True, blank = True)
	devision = models.CharField("Devision scolaire",max_length=50, choices=DEVISION_CHOICES, null=True, blank = True)

	def __str__(self):
		if self.devision:
			return '{},{},{},{}'.format(self.year,self.level,self.classe,self.devision)
		else:
			return '{},{},{}'.format(self.year,self.level,self.classe)

class Student(models.Model):
	GENDER_CHOICES = (
		("homme", "Homme"),
		("femme", "Femme")
	)
	parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name='fils')
	student_firstname = models.CharField("nom de l'eleve", max_length=200)
	student_name = models.CharField("prenom de l'eleve", max_length=200)
	date_of_birth = models.DateField("date de naissance de l'eleve",default=timezone.now)
	place_of_birth = models.CharField("Lieu de naissance de l'eleve", max_length=200)
	address = models.CharField("Adresse", max_length=300)
	allergic = models.TextField("Allergie à signaler",blank=True, null=True)
	chronical_sickness = models.TextField("maladie chronique à signaler",blank=True, null=True)
	particular_handicap = models.TextField("handicape particulier à signaler",blank=True, null=True)
	student_gender = models.CharField("le sexe de l'eleve",max_length=10, choices=GENDER_CHOICES, default="homme")
	study_level = models.OneToOneField(StudyLevel, on_delete=models.CASCADE, related_name='student', null=True, blank=True)
	student_avatar = models.ImageField("Image principale",upload_to = 'avatars/')
	scolar_inscription_date = models.DateField("date d'inscription scolaire",default=timezone.now)
	pedagogic_inscription_date = models.DateField("date d'inscription pedagogique",default=timezone.now)
	scolar_year = models.CharField("année scolaire",max_length=20, default="21/22")
	last_school_attended = models.CharField("dernière école fréquentée", max_length=400,blank=True, null=True)
	activities = models.ForeignKey("Activity", on_delete=models.CASCADE, related_name='fils',blank=True, null=True)

	def __str__(self):
		return '{}, {}'.format(self.student_firstname, self.parent.father_name)

	def get_full_name(self):
		return self.student_firstname + self.student_name

class Magazin(models.Model):
	nom_magazin = models.CharField(max_length=300)
	caisse = models.DecimalField(max_digits=100, decimal_places=2, default=0)
	created = models.DateField(default=timezone.now)
	updated = models.DateField(auto_now_add=False, auto_now=True)

	def __str__(self):
		return self.nom_magazin

	def get_total_entrant(self, year, month):
		factures = Abonement.objects.filter(
			date_de_creation__month=month,
			date_de_creation__year=year,
			magazin = self,
			status = 'validée et payée')
		total = 0
		for facture in factures:
			total = total + facture.somme_operation
		return total

	def get_total_sortant(self, year, month):
		total = 0
		factures = Facture.objects.filter(
			date_de_creation__month=month,
			date_de_creation__year=year,
			magazin = self,
			status = 'validée et payée')
		for facture in factures:
			total = total + facture.somme_operation
		return total

	def get_caisse(self, month = monthy):
		return self.caisse + self.get_total_entrant(yearly, month) - self.get_total_sortant(yearly, month)

class Villa (models.Model):
	nom_villa = models.CharField(max_length=200)
	magazin = models.OneToOneField(Magazin, on_delete=models.CASCADE,
				related_name="villa", blank=True, null=True)
	def __str__(self):
		return self.nom_villa

class Facture(models.Model):
	magazin = models.ForeignKey(Magazin, on_delete=models.CASCADE, related_name="factures_magazin")
	operateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="factures")
	somme_operation = models.DecimalField(max_digits=100, decimal_places=2)
	reste_a_paier = models.DecimalField(max_digits=100, decimal_places=2, default=0)
	description = models.CharField(max_length=200)
	date_de_creation = models.DateField(default=timezone.now)
	updated = models.DateField(auto_now_add=False, auto_now=True)
	status = models.CharField(
        max_length=30,
        choices=[("validée et payée", "Validée Et Payée"), ("pas encore", "Pas Encore")],
        default="validée et payée",
    )

	def __str__(self):
		return self.operateur.username + '|_-_|' + '___' + str(self.date_de_creation)

	def balance(self):
		return self.somme_operation - self.reste_a_paier



	def get_absolute_url(self):
		return reverse("detail de la facture", kwargs={"pk": self.pk})



class Classe(models.Model):
	nom_classe = models.CharField(max_length=200)
	prix_categorie = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.nom_classe

class Matiere(models.Model):
	nom_matiere = models.CharField(max_length=300, default='')
	prix_matiere = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return self.nom_matiere

class Cours_particulier(models.Model):
	matiere = models.ForeignKey("Matiere", on_delete=models.CASCADE, verbose_name="matiere", related_name="courses")
	classe = models.ForeignKey("Classe", on_delete=models.CASCADE, verbose_name="classe", related_name="courses", null=True, blank=True)
	nom_etudiant = models.CharField(max_length=200)
	prenom_etudiant = models.CharField(max_length=200)

	def get_full_name(self):
		return self.nom_etudiant + self.prenom_etudiant

	def __str__(self):
		return "etudiant {} ,matiere{}".format(self.get_full_name(),self.matiere)

class Activity(models.Model):
	activity_name = models.CharField("nom de l'activité", max_length=200)
	activity_price = models.DecimalField(max_digits=8, decimal_places=2)

class Abonement(models.Model):
	magazin = models.ForeignKey(Magazin, on_delete=models.CASCADE, related_name="abonements_magazin")
	operateur = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="abonements")
	somme_operation = models.DecimalField(max_digits=100, decimal_places=2)
	reste_a_paier = models.DecimalField(max_digits=100, decimal_places=2, default=0)
	description = models.CharField(max_length=200)
	date_de_creation = models.DateField(default=timezone.now)
	updated = models.DateField(auto_now_add=False, auto_now=True)
	status = models.CharField(
        max_length=30,
        choices=[("validée et payée", "Validée Et Payée"), ("pas encore", "Pas Encore")],
        default="validée et payée",
    )

	def __str__(self):
		return self.operateur.father_name + '|_-_|' + '___' + str(self.date_de_creation)

	def balance(self):
		return self.somme_operation - self.reste_a_paier



	def get_absolute_url(self):
		return reverse("detail de la facture", kwargs={"pk": self.pk})