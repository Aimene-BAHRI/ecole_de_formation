# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import imp
from tkinter.messagebox import NO
from django import template
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Sum
from datetime import date, datetime
monthy = datetime.today().month
yearly = datetime.today().year

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

    parants = Parent.objects.all()
    students = Student.objects.all()
    magazins = Magazin.objects.all()
    factures = Facture.objects.filter(
        date_de_creation__month=monthy,
        date_de_creation__year=yearly)
    monthly_gain_data = []
    total_gain_monthly = 0
    for magazin in magazins:
        total_gain_monthly += magazin.get_caisse()

    for current_month in range(1,13):
        gain_totale = 0
        for magazin in magazins:
            gain_totale = gain_totale + magazin.get_caisse(current_month)
        monthly_gain_data.append(float(gain_totale))

    print(monthly_gain_data)

    context = {
        'segment': 'dashboard',
        'parants' : parants,
        'parants_count' : parants.count(),
        'students' : students,
        'students_count' : students.count(),
        'magazins' : magazins,
        'magazins_count' : magazins.count(),
        'factures' : factures,
        'factures_count' : factures.count(),
        'gain_totale' : total_gain_monthly,
        'monthly_gain_data' : monthly_gain_data

    }

    html_template = loader.get_template('home/dashboard.html')
    return HttpResponse(html_template.render(context, request))

# Administrations CRUD
# PARANT
@login_required(login_url='login')
def create_parant(request):
    parant_form = ParentForm()
    user_form = SignUpForm()
    print('HI')
    if request.method == 'POST':
        print('post request')
        parant_form = ParentForm(request.POST or None, request.FILES)
        user_form = SignUpForm(request.POST or None)
        if user_form.is_valid() and parant_form.is_valid():
            print('validation request')
            user_instance = user_form.save()

            parant = parant_form.save(commit=False)
            parant.user = user_instance
            parant.save()
            return redirect(reverse('parants'))
        else:
            print(parant_form.errors)
            print(user_form.errors)

    context = {
        'segment' : 'create_parant',
        'user_form' : user_form,
        'parant_form' : parant_form
    }

    html_template = loader.get_template('home/parant/create_parant.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def parants(request):
    parants = Parent.objects.all()
    context = {
        'segment': 'parants',
        'parants' : parants,
    }

    html_template = loader.get_template('home/parant/parants.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def parant(request, pk):
    parant = Parent.objects.get(id= pk)
    parant_form = ParentForm(instance=parant)
    print('HI')
    if request.method == 'POST':
        print('post request')
        parant_form = ParentForm(request.POST or None, request.FILES, instance=parant)
        if parant_form.is_valid():
            print('validation request')
            parant = parant_form.save(commit=False)
            parant.save()
            return redirect(reverse('parants'))
        else:
            print(parant_form.errors)
    context = {
        'segment': 'parants',
        'parant' : parant,
        'parant_form' : parant_form
    }

    html_template = loader.get_template('home/parant/parant.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='login')
def delete_parant(request, pk):
    object = Parent.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('parants'))
    return render(request,'home/Object_delete.html',{'object': object})

@login_required(login_url="login")
def profile(request):
    user_profile_form = UserProfileForm(instance=request.user)
    try:
        parent = Parent.objects.get(user = request.user)
    except Parent.DoesNotExist:
        parent = None
    context = {
        'segment' : 'profile',
        'user' : request.user,
        'parent' : parent,

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
    try:
        parant = Parent.objects.get(user = user)
        mes_enfants = parant.fils.all()
    except Parent.DoesNotExist:
        parant = None
        mes_enfants = []

    context = {
        'segment' : 'mes_enfants',
        'user' : request.user,
        'mes_enfants' : mes_enfants,
    }
    html_template = loader.get_template('home/mes_enfants.html')
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



@login_required(login_url="/login/")
def export_pdf(request, pk):
    if request.user.is_superuser:
        print('hahaha admin')
        facture = Facture.objects.get(pk = pk)
        return render_to_pdf_response(request,'home/renderdetail.html', {'invoice':facture})
    else:
        try:
            facture = Facture.objects.get(pk = pk, operateur = request.user)
            return render_to_pdf_response(request,'home/renderdetail.html', {'invoice':facture})
        except Facture.DoesNotExist:
            return redirect(reverse('mes_factures'))


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
    students = Student.objects.all()
    context = {
        'segment': 'students',
        'students' : students
    }

    html_template = loader.get_template('home/student/students.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def student(request, pk):
    student = Student.objects.get(id= pk)
    student_form = StudentForm(request.POST or None, instance = student)
    if request.method == 'POST':
        student_form = StudentForm(request.POST or None, instance=student)
        if student_form.is_valid() :
            student_form.save()
        return redirect(reverse('students'))
    context = {
        'segment': 'students',
        'student' : student,
        'student_form' : student_form
    }

    html_template = loader.get_template('home/student/student.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url='login')
def delete_student(request, pk):
    object = Student.objects.get(id = pk)
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
        'magazins' : magazins,
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
        'segment' : 'magazins',
        'magazin_form' : magazin_form,
        'magazin' : magazin
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
        'segment' : 'factures',
        'facture_form' : facture_form,
        'facture' : facture
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



# Matiere
@login_required(login_url='login')
def create_matiere(request):
    matiere_form = MatiereForm()
    if request.method == 'POST':
        matiere_form = MatiereForm(request.POST or None)
        if matiere_form.is_valid() :
            matiere_form.save()
        return redirect(reverse('matieres'))

    context = {
        'segment' : 'create_matiere',
        'matiere_form' : matiere_form,
    }

    html_template = loader.get_template('home/matiere/create_matiere.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def matieres(request):
    matieres = Matiere.objects.all()
    context = {
        'segment': 'matieres',
        'matieres' : matieres
    }

    html_template = loader.get_template('home/matiere/matieres.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def matiere(request, pk):
    matiere = get_object_or_404(Matiere, pk = pk)
    matiere_form = MatiereForm(instance=matiere)
    if request.method == 'POST':
        matiere_form = MatiereForm(request.POST or None, instance=matiere)
        if matiere_form.is_valid() :
            matiere_form.save()
        return redirect(reverse('matieres'))

    context = {
        'segment' : 'matieres',
        'matiere_form' : matiere_form,
        'matiere' : matiere
    }

    html_template = loader.get_template('home/matiere/matiere.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def delete_matiere(request, pk):
    object = Matiere.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('matieres'))
    return render(request,'home/Object_delete.html',{'object': object})

# Cours_particulier
@login_required(login_url='login')
def create_cours(request):
    cours_form = Cours_particulierForm()
    if request.method == 'POST':
        cours_form = Cours_particulierForm(request.POST or None)
        if cours_form.is_valid() :
            cours_form.save()
        return redirect(reverse('courses'))

    context = {
        'segment' : 'create_cours',
        'cours_form' : cours_form,
    }

    html_template = loader.get_template('home/cours/create_cours.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def courses(request):
    courses = Cours_particulier.objects.all()
    context = {
        'segment': 'courses',
        'courses' : courses
    }

    html_template = loader.get_template('home/cours/courses.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def cours(request, pk):
    cours = get_object_or_404(Cours_particulier, pk = pk)
    cours_form = Cours_particulierForm(instance=cours)
    if request.method == 'POST':
        cours_form = Cours_particulierForm(request.POST or None, instance=cours)
        if cours_form.is_valid() :
            cours_form.save()
        return redirect(reverse('courses'))

    context = {
        'segment' : 'courses',
        'cours_form' : cours_form,
        'cours' : cours
    }

    html_template = loader.get_template('home/cours/cours.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def delete_cours(request, pk):
    object = Cours_particulier.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('courses'))
    return render(request,'home/Object_delete.html',{'object': object})

# Activity
@login_required(login_url='login')
def create_activity(request):
    activity_form = ActivityForm()
    if request.method == 'POST':
        activity_form = ActivityForm(request.POST or None)
        if activity_form.is_valid() :
            activity_form.save()
        return redirect(reverse('activities'))

    context = {
        'segment' : 'create_activity',
        'activity_form' : activity_form,
    }

    html_template = loader.get_template('home/activity/create_activity.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def activities(request):
    activities = Activity.objects.all()
    context = {
        'segment': 'activities',
        'activities' : activities
    }

    html_template = loader.get_template('home/activity/activities.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def activity(request, pk):
    activity = get_object_or_404(Activity, pk = pk)
    activity_form = ActivityForm(instance=activity)
    if request.method == 'POST':
        activity_form = ActivityForm(request.POST or None, instance=activity)
        if activity_form.is_valid() :
            activity_form.save()
        return redirect(reverse('activities'))

    context = {
        'segment' : 'activities',
        'activity_form' : activity_form,
        'activity' : activity
    }

    html_template = loader.get_template('home/activity/activity.html')
    return HttpResponse(html_template.render(context, request))

@login_required(login_url='login')
def delete_activity(request, pk):
    object = Activity.objects.get(id = pk)
    if request.method == 'POST':
        object.delete()
        return redirect(reverse('activities'))
    return render(request,'home/Object_delete.html',{'object': object})