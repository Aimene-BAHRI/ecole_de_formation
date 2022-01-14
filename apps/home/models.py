# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.urls import reverse
# Create your models here.

class Parant(models.Model):
	user = models.OneToOneField(User, verbose_name="utilisateur", on_delete=models.CASCADE, related_name="parant")
	nom_parent = models.CharField("nom du parant", max_length=100)
	prenom_parent = models.CharField("prénom du parant", max_length=100)
	telephone = models.CharField("numéro de téléphone", max_length=20)

	def __str__(self):
		return '{}, {}'.format(self.prenom_parent, self.nom_parent)

	def get_total_a_payer(self):
		factures = Facture.objects.filter(operateur = self)
		total = 0
		for facture in factures:
			total = total + facture.somme_operation
		return total

	def get_fils_count(self):
		fils = self.fils.all().count()
		return fils
class Fils(models.Model):
	GENDER_CHOICES = (
		("male", "Male"), 
		("female", "Female")
	)
	NIVEAU_CHOICES = (
		("prescolaire", "Prescolaire"),
		("preparatoire", "Preparatoire"), 
		("primaire", "Primaire"),
		("moyenne", "Moyenne"),
		("lycéenne", "Lycéenne")
	)
	parant = models.ForeignKey(Parant, on_delete=models.CASCADE, related_name='fils')
	prenom_fils = models.CharField("nom fils", max_length=200)
	gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
	date_of_birth = models.DateField(default=timezone.now)
	niveau_etude = models.CharField("niveau d'etude", max_length=200, choices=NIVEAU_CHOICES, default='prescolaire')
	matiere = models.ManyToManyField("Matiere", verbose_name="matiere", related_name="etudiants")

	def __str__(self):
		return '{}, {}'.format(self.prenom_fils, self.parant.prenom_parent)

	def get_full_name(self):
		return self.parant.nom_parent + self.prenom_etudiant

class Matiere(models.Model):
	nom_matiere = models.CharField(max_length=300, default='')
	prix_matiere = models.DecimalField(max_digits=8, decimal_places=2)

	def __str__(self):
		return self.nom_matiere

class Magazin(models.Model):
	nom_magazin = models.CharField(max_length=300)
	caisse = models.DecimalField(max_digits=100, decimal_places=2, default=0)

	def __str__(self):
		return self.nom_magazin
	
	def get_total_entrant(self):
		factures = Facture.objects.filter(magazin = self, type_operation = 'entrée')
		total = 0
		for facture in factures:
			total = total + facture.somme_operation
		return total
	
	def get_total_sortant(self):
		total = 0
		factures = Facture.objects.filter(magazin = self, type_operation = 'sortie')
		for facture in factures:
			total = total + facture.somme_operation
		return total
	
class Facture(models.Model):
	magazin = models.ForeignKey(Magazin, on_delete=models.CASCADE, related_name="factures_magazin")
	operateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name="factures")
	type_operation = models.CharField(max_length=20, choices=(("entrée", "entrée"), ("sortie" , "sortie")), default='sortie')
	somme_operation = models.DecimalField(max_digits=100, decimal_places=2)
	description = models.CharField(max_length=200)
	date_de_creation = models.DateField(auto_now_add=True)
	status = models.CharField(
        max_length=20,
        choices=[("active", "Active"), ("closed", "Closed")],
        default="active",
    )

	def __str__(self):
		return self.operateur.username + '|_-_|' + self.type_operation + '___' + str(self.date_de_creation)
	
	def balance(self):
		payable = self.total_amount_payable()
		paid = self.total_amount_paid()
		return payable - paid

	def amount_payable(self):
		items = InvoiceItem.objects.filter(invoice=self)
		total = 0
		for item in items:
			total += item.amount
		return total

	def total_amount_payable(self):
		return self.balance_from_previous_term + self.amount_payable()

	def total_amount_paid(self):
		receipts = Receipt.objects.filter(invoice=self)
		amount = 0
		for receipt in receipts:
			amount += receipt.amount_paid
		return amount


	def get_absolute_url(self):
		return reverse("detail de la facture", kwargs={"pk": self.pk})

class InvoiceItem(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.IntegerField()

class Receipt(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    amount_paid = models.IntegerField()
    date_paid = models.DateField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Reçu le  {self.date_paid}"

class Cours_particulier(models.Model):
	matiere = models.ForeignKey("Matiere", on_delete=models.CASCADE, verbose_name="matiere", related_name="courses")
	categorie = models.ForeignKey("Categorie", on_delete=models.CASCADE, verbose_name="categorie", related_name="etudiants")
	nom_etudiant = models.CharField(max_length=200)
	prenom_etudiant = models.CharField(max_length=200)

	def get_full_name(self):
		return self.nom_etudiant + self.prenom_etudiant

	def __str__(self):
		return "etudiant {} ,matiere{}".format(self.get_full_name(),self.matiere)
	
class Categorie(models.Model):
	nom_categorie = models.CharField(max_length=200)
	prix_categorie = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.nom_categorie