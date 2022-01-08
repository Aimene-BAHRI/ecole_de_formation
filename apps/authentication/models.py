# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models

# Create your models here.
# class Parant(models.Model):
# 	user = models.OneToOneField("User", verbose_name="utilisateur", on_delete=models.CASCADE, related_name="parant")
# 	nom_parent = models.CharField("nom du parant", max_length=100)
# 	prenom_parent = models.CharField("nom du parant", max_length=100)
# 	telephone = models.CharField("numero de telephone", max_length=20)
# 	fils = models.ForeignKey("Fils", verbose_name="fils", on_delete=models.PROTECT, related_name='parant')

# 	def __str__(self):
# 		return self.user.username

# class Fils(models.Model):
# 	prenom_fils = models.CharField("nom fils", max_length=200)
# 	matiere = models.CharField()