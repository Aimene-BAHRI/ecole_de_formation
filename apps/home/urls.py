# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Parant
    path('parants/create', views.create_parant, name="create_parant"),
    path('parants/', views.parants, name="parants"),
    path('parants/<pk>', views.parant, name="parant"),
    path('parants/delete/<pk>', views.delete_parant, name="delete_parant"),

    # Student
    path('students/', views.students, name="students"),
    path('students/create', views.create_student, name="create_student"),
    path('students/<pk>', views.student, name="student"),
    path('students/delete/<pk>', views.delete_student, name="delete_student"),

    # Magazin
    path('magazins/', views.magazins, name="magazins"),
    path('magazins/create', views.create_magazin, name="create_magazin"),
    path('magazins/<pk>', views.magazin, name="magazin"),
    path('magazins/delete/<pk>', views.delete_magazin, name="delete_magazin"),

    # Facture
    path('factures/', views.factures, name="factures"),
    path('factures/create', views.create_facture, name="create_facture"),
    path('factures/<pk>', views.facture, name="facture"),
    path('factures/delete/<pk>', views.delete_facture, name="delete_facture"),

    # Abonement
    path('abonements/', views.abonements, name="abonements"),
    path('abonements/create', views.create_abonement, name="create_abonement"),
    path('abonements/<pk>', views.abonement, name="abonement"),
    path('abonements/delete/<pk>', views.delete_abonement, name="delete_abonement"),

    # Matiere
    path('matieres/', views.matieres, name="matieres"),
    path('matieres/create', views.create_matiere, name="create_matiere"),
    path('matieres/update/<pk>', views.matiere, name="matiere"),
    path('matieres/delete/<pk>', views.delete_matiere, name="delete_matiere"),

    # Cours_Particulier
    path('courses/', views.courses, name="courses"),
    path('courses/create', views.create_cours, name="create_cours"),
    path('courses/update/<pk>', views.cours, name="cours"),
    path('courses/delete/<pk>', views.delete_cours, name="delete_cours"),

    # Parent SIMPLE UDAGE URLS
    path('profile/', views.profile, name='profile'),
    path('mes_factures/', views.mes_factures, name='mes_factures'),
    path('mes_factures/<pk>', views.facture_detail, name='facture_detail'),
    path('export_pdf/<pk>', views.export_pdf, name='export'),
    path('export_pdf_abonement/<pk>', views.export_pdf_abonement, name='export_pdf_abonement'),
    path('mes_enfants/', views.mes_enfants, name='mes_enfants'),

    # Activity
    path('activities/', views.activities, name="activities"),
    path('activities/create', views.create_activity, name="create_activity"),
    path('activities/update/<pk>', views.activity, name="activity"),
    path('activities/delete/<pk>', views.delete_activity, name="delete_activity"),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
