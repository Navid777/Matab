# -*- coding: utf-8 -*-
from django.http.response import Http404
from Radiology.forms import LoginForm, PatientForm, InsuranceForm, \
    AppointmentForm, TherapistForm, OperationForm, PatientPartialForm
from Radiology.models import Insurance, Patient, Appointment, Doctor, Therapist,\
    Operation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from datetime import datetime
from accounting import interface as accounting

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
            return HttpResponseRedirect('/home/')
    else:
        form = LoginForm()
    return render(request, "login.html", {'form': form})


@login_required
def home(request):
    insurance_types = Insurance.objects.values_list('type', flat=True).distinct()
    return render(request, 'home.html', {
        "insurance_types": insurance_types,
    })


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required
def appointment_day(request):
    return render(request, 'appointment_day.html', {})

@login_required
def appointment(request, day):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        form.set_day(datetime.strptime(day, '%Y-%m-%d'))
        if form.is_valid():
            doctor = Doctor.objects.all()[0]
            app = Appointment.objects.create(
                patient=Patient.objects.get(id=request.session['current_patient']),
                doctor=doctor,
                day=datetime.strptime(day, '%Y-%m-%d'),
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
            )
            return HttpResponseRedirect('/appointment/')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {
        'day': day,
        'form': form,
        'apps': Appointment.objects.filter(day=datetime.strptime(day, '%Y-%m-%d'))
    })


def insurance_categories(request):
    if request.method == 'GET':
        if 'insurance_type' in request.GET:
            return HttpResponse(
                serializers.serialize("xml", Insurance.objects.filter(insurance_type=request.GET['insurance_type'])))
        else:
            pass


@login_required
def ajax_find_patients_by_name(request):
    if request.method != "POST":
        raise Http404()
    form = PatientPartialForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        patients = Patient.objects.filter(first_name=cd['first_name'], last_name=cd['last_name'])
        return render(request, 'json/find_patients.json', {
            'patients': patients
        })
    return render(request, 'json/error.json', {})


@login_required
def ajax_find_insurance_categories_by_type(request):
    if request.method != "POST":
        raise Http404()
    type = request.POST['type']
    categories = Insurance.objects.filter(type=type).values_list('category', flat=True).distinct()
    return render(request, 'json/insurance_categories.json', {
        'categories': categories,
    })