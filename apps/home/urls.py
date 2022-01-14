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
    path('parants/', views.parants, name="parants"),
    path('create_parant/', views.create_parant, name="create_parant"),
    
    
    path('profile/', views.profile, name='profile'),
    path('mes_factures/', views.mes_factures, name='mes_factures'),
    path('mes_factures/<pk>', views.facture_detail, name='facture_detail'),
    path('export_pdf/<pk>', views.export_pdf, name='export'),
    path('mes_enfants/', views.mes_enfants, name='mes_enfants'),

    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
