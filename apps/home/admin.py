# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from .models import Parent, Student,Magazin,Facture,InvoiceItem, Receipt, Cours_particulier, Classe



admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Magazin)
admin.site.register(Facture)
admin.site.register(InvoiceItem)
admin.site.register(Receipt)
admin.site.register(Cours_particulier)
admin.site.register(Classe)

