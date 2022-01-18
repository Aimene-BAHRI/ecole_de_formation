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
    # parants
    path('parants/create', views.create_parant, name="create_parant"),
    path('parants/', views.parants, name="parants"),
    path('parants/<pk>', views.parant, name="parant"),
    # path('parants/update/<pk>', views.update_parant, name="update_parant"),
    path('parants/delete/<pk>', views.delete_parant, name="delete_parant"),
    # Fils
    path('students/', views.students, name="students"),
    path('students/create', views.create_student, name="create_student"),
    path('students/<pk>', views.student, name="student"),
    # path('students/update/<pk>', views.update_student, name="update_student"),
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

    # Matiere
    # path('matieres/', views.delete_parant, name="delete_parant"),
    # path('matieres/create', views.delete_parant, name="delete_parant"),
    # path('matieres/update/<pk>', views.delete_parant, name="delete_parant"),
    # path('matieres/delete/<pk>', views.delete_parant, name="delete_parant"),

    # Parant SIMPLE UDAGE URLS
    path('profile/', views.profile, name='profile'),
    path('mes_factures/', views.mes_factures, name='mes_factures'),
    path('mes_factures/<pk>', views.facture_detail, name='facture_detail'),
    path('export_pdf/<pk>', views.export_pdf, name='export'),
    path('mes_enfants/', views.mes_enfants, name='mes_enfants'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
