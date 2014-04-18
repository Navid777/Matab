# -*- coding: utf-8 -*-
from Radiology.forms import LoginForm, PatientForm, InsuranceForm, \
    AppointmentForm, TherapistForm, OperationForm
from Radiology.models import Insurance, Patient, Appointment, Doctor, Therapist,\
    Operation
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


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
    patient_form = PatientForm()
    therapist_form = TherapistForm()
    operation_form = OperationForm()
    insurance_form = InsuranceForm()
    operations = Operation.objects.all()
    insurances = Insurance.objects.all()
    if 'current_patient' in request.session:
        try :
            patient = Patient.objects.get(id=request.session['current_patient'])
        except Patient.DoesNotExist:
            del request.session['current_patient']
            patient = None
    else:
        patient = None
    if 'current_therapist' in request.session:
        try :
            therapist = Therapist.objects.get(id=request.session['current_therapist'])
        except Therapist.DoesNotExist:
            del request.session['current_therapist']
            therapist = None
    else:
        therapist = None
    if request.method == 'POST' and 'patient_signup' in request.POST:
        patient_form = PatientForm(request.POST)
        if patient_form.is_valid():
            cd = patient_form.cleaned_data
            new_patient = Patient()
            new_patient.first_name = cd['patient_first_name']
            new_patient.last_name = cd['patient_last_name']
            new_patient.national_code = cd['patient_national_code']
            new_patient.save()
            request.session['current_patient'] = new_patient.id
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'patient_login' in request.POST:
        patient_form = PatientForm(request.POST)
        if patient_form.is_valid():
            cd = patient_form.cleaned_data
            request.session['current_patient'] = cd['patient_id']
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'new_patient' in request.POST:
        del request.session['current_patient']
        return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'new_therapist' in request.POST:
        del request.session['current_therapist']
        return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'therapist_signup' in request.POST:
        therapist_form = TherapistForm(request.POST)
        if therapist_form.is_valid():
            cd = therapist_form.cleaned_data
            new_therapist = Therapist()
            new_therapist.medical_number = cd['therapist_medical_number']
            new_therapist.first_name = cd['therapist_first_name']
            new_therapist.last_name = cd['therapist_last_name']
            new_therapist.save()
            request.session['current_therapist'] = new_therapist.id
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'therapist_login' in request.POST:
        therapist_form = TherapistForm(request.POST)
        if therapist_form.is_valid():
            cd = therapist_form.cleaned_data
            request.session['current_therapist'] = cd['therapist_id']
            return HttpResponseRedirect('/home/')
    return render(request, 'home.html', {'patient_form': patient_form, 
                                         'patient':patient,
                                         'insurance_form': insurance_form, 
                                         'therapist_form':therapist_form,
                                         'operation_form':operation_form,
                                         'therapist':therapist,
                                         'insurances':insurances,
                                         'operations':operations})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')


@login_required
def appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            doctor = Doctor.objects.all()[0]
            print form.cleaned_data
            import datetime

            app = Appointment.objects.create(
                patient=Patient.objects.get(id=request.session['current_patient']),
                doctor=doctor,
                day=datetime.datetime.now(),
                start_time=form.cleaned_data['start_time'],
                end_time=form.cleaned_data['end_time'],
            )
            return HttpResponseRedirect('/appointment/')
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {
        'form': form,
        'apps': Appointment.objects.all()
    })


def insurance_categories(request):
    if request.method == 'GET':
        if 'insurance_type' in request.GET:
            return HttpResponse(
                serializers.serialize("xml", Insurance.objects.filter(insurance_type=request.GET['insurance_type'])))
        else:
            pass
