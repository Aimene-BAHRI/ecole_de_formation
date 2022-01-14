# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import *
from .forms import *
@login_required(login_url="login")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="login")
def dashboard(request):
    context = {'segment': 'dashboard'}

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def parants(request):
    context = {'segment': 'parants'}

    html_template = loader.get_template('home/parant/parants.html')
    return HttpResponse(html_template.render(context, request))

# Administrations CRUD
@login_required(login_url='login')
def create_parant(request):
    parant_form = ParantForm()
    user_form = UserCreationForm()
    print('HI')
    context = {
        'segment' : 'create_parant',
        'user_form' : user_form,
        'parant_form' : parant_form
    }

    html_template = loader.get_template('home/parant/create_parant.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="login")
def profile(request):
    user_profile_form = UserProfileForm(instance=request.user)
    context = {
        'segment' : 'profile',
        'user' : request.user,
        'form' : user_profile_form,

    }
    html_template = loader.get_template('home/profile.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def mes_factures(request):
    mes_factures = request.user.factures.all()
    context = {
        'segment' : 'mes_factures',
        'user' : request.user,
        'mes_factures' : mes_factures,
    }
    html_template = loader.get_template('home/mes_factures.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def mes_enfants(request):
    user = request.user
    parant = Parant.objects.get(user = user)
    mes_enfants = parant.fils.all()
    context = {
        'segment' : 'mes_enfants',
        'user' : request.user,
        'mes_enfants' : mes_enfants,
    }
    html_template = loader.get_template('home/mes_factures.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def facture_detail(request, pk):
    facture = Facture.objects.get(pk = pk)
    print(facture)
    context = {
        'segment' : 'facture_detail',
        'user' : request.user,
        'invoice' : facture,
    }
    html_template = loader.get_template('home/facture_detail.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

from easy_pdf.rendering import render_to_pdf_response



def export_pdf(request, pk):
    facture = Facture.objects.get(pk = pk)
    return render_to_pdf_response(request,'home/renderdetail.html', {'invoice':facture})



