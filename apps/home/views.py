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
from django.shortcuts import get_object_or_404, render, redirect


from apps.authentication.forms import SignUpForm
from .models import *
from .forms import *
@login_required(login_url="login")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

from django.contrib.auth.decorators import user_passes_test
def staff_required(login_url=None):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

@staff_required(login_url="login")
@login_required(login_url="login")
def dashboard(request):
    parants = Parant.objects.all()
    students = Fils.objects.all()
    magazins = Magazin.objects.all()
    factures = Facture.objects.all()

    context = {
        'segment': 'dashboard',
        'parants' : parants,
        'parants_count' : parants.count(),
        'students' : students,
        'students_count' : students.count(),
        'magazins' : magazins,
        'magazins_count' : magazins.count(),
        'factures' : factures,
        'factures_count' : factures.count()

    }

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))

# Administrations CRUD
# PARANT
@login_required(login_url='login')
def create_parant(request):
    parant_form = ParantForm()
    user_form = SignUpForm()
    print('HI')
    if request.method == 'POST':
        parant_form = ParantForm(request.POST or None)
        user_form = SignUpForm(request.POST or None)
        if user_form.is_valid() and parant_form.is_valid():
            user_instance = user_form.save()

            parant = parant_form.save(commit=False)
            parant.user = user_instance
            parant.save()
        return redirect(reverse('parants'))

    context = {
        'segment' : 'create_parant',
        'user_form' : user_form,
        'parant_form' : parant_form
    }

    html_template = loader.get_template('home/parant/create_parant.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def parants(request):
    parants = Parant.objects.all()
    context = {
        'segment': 'parants',
        'parants' : parants    
    }

    html_template = loader.get_template('home/parant/parants.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def create_parant(request):
    parant_form = ParantForm()
    user_form = SignUpForm()
    print('HI')
    if request.method == 'POST':
        parant_form = ParantForm(request.POST or None)
        user_form = SignUpForm(request.POST or None)
        if user_form.is_valid() and parant_form.is_valid():
            user_instance = user_form.save()

            parant = parant_form.save(commit=False)
            parant.user = user_instance
            parant.save()
        return redirect(reverse('parants'))

    context = {
        'segment' : 'create_parant',
        'user_form' : user_form,
        'parant_form' : parant_form
    }

    html_template = loader.get_template('home/parant/create_parant.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def parant(request, pk):
    parant = Parant.objects.get(id= pk)
    context = {
        'segment': 'parant',
        'parant' : parant   
    }

    html_template = loader.get_template('home/parant/parant.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='login')
def delete_parant(request, pk):
    object = Parant.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('parants'))
    return render(request,'home/Object_delete.html',{'object': object})

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

# FILS
def create_student(request):
    student_form = StudentForm()
    if request.method == 'POST':
        student_form = StudentForm(request.POST or None)
        if student_form.is_valid() :
            student_form.save()
            return redirect(reverse('students'))
        else:
            print(student_form.errors)
    context = {
        'segment' : 'create_magazin',
        'student_form' : student_form,
    }
    html_template = loader.get_template('home/student/create_student.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def students(request):
    students = Fils.objects.all()
    context = {
        'segment': 'students',
        'students' : students    
    }

    html_template = loader.get_template('home/student/students.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def student(request, pk):
    student = Fils.objects.get(id= pk)
    student_form = StudentForm(request.POST or None, instance = student)
    if request.method == 'POST':
        student_form = StudentForm(request.POST or None, instance=student)
        if student_form.is_valid() :
            student_form.save()
        return redirect(reverse('students'))
    context = {
        'segment': 'student',
        'student' : student,
        'student_form' : student_form   
    }

    html_template = loader.get_template('home/student/student.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='login')
def delete_student(request, pk):
    object = Fils.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('students'))
    return render(request,'home/Object_delete.html',{'object': object})

# MAGAZIN
@login_required(login_url='login')
def create_magazin(request):
    magazin_form = MagazinForm()
    if request.method == 'POST':
        magazin_form = MagazinForm(request.POST or None)
        if magazin_form.is_valid() :
            magazin_form.save()
        return redirect(reverse('magazins'))

    context = {
        'segment' : 'create_magazin',
        'magazin_form' : magazin_form,
    }

    html_template = loader.get_template('home/magazin/create_magazin.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def magazins(request):
    magazins = Magazin.objects.all()
    context = {
        'segment': 'magazins',
        'magazins' : magazins    
    }

    html_template = loader.get_template('home/magazin/magazins.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def magazin(request, pk):
    magazin = get_object_or_404(Magazin, pk = pk)
    magazin_form = MagazinForm(instance=magazin)
    if request.method == 'POST':
        magazin_form = MagazinForm(request.POST or None, instance=magazin)
        if magazin_form.is_valid() :
            magazin_form.save()
        return redirect(reverse('magazins'))

    context = {
        'segment' : 'magazin',
        'magazin_form' : magazin_form,
    }

    html_template = loader.get_template('home/magazin/magazin.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def delete_magazin(request, pk):
    object = Magazin.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('magazins'))
    return render(request,'home/Object_delete.html',{'object': object})

# FACTURE
@login_required(login_url='login')
def create_facture(request):
    facture_form = FactureForm()
    if request.method == 'POST':
        facture_form = FactureForm(request.POST or None)
        if facture_form.is_valid() :
            facture_form.save()
        return redirect(reverse('factures'))

    context = {
        'segment' : 'create_facture',
        'facture_form' : facture_form,
    }

    html_template = loader.get_template('home/facture/create_facture.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def factures(request):
    factures = Facture.objects.all()
    context = {
        'segment': 'factures',
        'factures' : factures    
    }

    html_template = loader.get_template('home/facture/factures.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def facture(request, pk):
    facture = get_object_or_404(Facture, pk = pk)
    facture_form = FactureForm(instance=facture)
    if request.method == 'POST':
        facture_form = FactureForm(request.POST or None, instance=facture)
        if facture_form.is_valid() :
            facture_form.save()
        return redirect(reverse('factures'))

    context = {
        'segment' : 'facture',
        'facture_form' : facture_form,
    }

    html_template = loader.get_template('home/facture/facture.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def delete_facture(request, pk):
    object = Facture.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('factures'))
    return render(request,'home/Object_delete.html',{'object': object})