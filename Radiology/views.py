# -*- coding: utf-8 -*-
from Radiology.forms import LoginForm, PatientForm, InsuranceForm, AppointmentForm,\
    TherapistForm, OperationForm
from Radiology.models import Patient, Appointment, Doctor
from Radiology.models import Insurance
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from datetime import datetime

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
    if request.method == 'POST' and 'sabt' in request.POST:
        patient_form = PatientForm(request.POST)
        therapist_form = TherapistForm()
        insurance_form = InsuranceForm()
        operation_form = OperationForm()
        if patient_form.is_valid():
            cd = patient_form.cleaned_data
            patient = Patient()
            patient.first_name = cd['patient_first_name']
            patient.last_name = cd['patient_last_name']
            patient.national_code = cd['patient_national_code']
            patient.save()
            request.session['current_patient'] = patient.id
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'vorood' in request.POST:
        patient_form = PatientForm(request.POST)
        insurance_form = InsuranceForm()
        therapist_form = TherapistForm()
        operation_form = OperationForm()
        if patient_form.is_valid():
            cd = patient_form.cleaned_data
            request.session['current_patient'] = cd['patient_id']
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'jadid' in request.POST:
        del request.session['current_patient']
        return HttpResponseRedirect('/home/')
    else:
        insurance_form = InsuranceForm()
        therapist_form = TherapistForm()
        operation_form = OperationForm()
        patient_form = PatientForm()
        if not 'current_patient' in request.session:
            has_patient = False
            patient = Patient()
        else:
            has_patient = True
            try:
                patient = Patient.objects.get(id=request.session['current_patient'])
            except Patient.DoesNotExist:
                del request.session['current_patient']
                HttpResponseRedirect('/home/')
    return render(request, 'home.html', {'has_patient':has_patient,'patient_form': patient_form, 
                                         'patient':patient,
                                         'insurance_form': insurance_form, 
                                         'therapist_form':therapist_form,
                                         'operation_form':operation_form})


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
