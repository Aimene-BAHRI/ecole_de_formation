# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import Abonement, Parent, Student,Magazin,Facture, Cours_particulier, Classe, StudyLevel



admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Magazin)
admin.site.register(Facture)
admin.site.register(Abonement)
admin.site.register(Cours_particulier)
admin.site.register(Classe)
admin.site.register(StudyLevel)

