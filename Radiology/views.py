# -*- coding: utf-8 -*-
from Radiology.forms import LoginForm, PatientForm, InsuranceForm, \
    AppointmentForm, TherapistForm, OperationForm, PatientPartialForm
from Radiology.models import Insurance, Patient, Appointment, Doctor, Therapist, \
    Operation
from accounting import interface as accounting
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, Http404
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
def home(request):
    patient_form = PatientForm()
    therapist_form = TherapistForm()
    operation_form = OperationForm()
    insurance_form = InsuranceForm()
    operations = Operation.objects.all()
    insurances = Insurance.objects.all()
    if 'current_patient' in request.session:
        try:
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
    if 'current_insurance' in request.session:
        try:
            insurance = Insurance.objects.get(id=request.session['current_insurance'])
        except Insurance.DoesNotExist:
            del request.session['current_insurance']
            insurance = None
    else:
        insurance = None
    if request.method == 'POST' and 'patient_signup' in request.POST:
        patient_form = PatientForm(request.POST)
        if patient_form.is_valid():
            cd = patient_form.cleaned_data
            account_id = accounting.create_account(Patient.ACCOUNT_SERIES)
            new_patient = Patient.objects.create(
                first_name=cd['patient_first_name'],
                last_name=cd['patient_last_name'],
                national_code=cd['patient_national_code'],
                account_id=account_id
            )
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
            new_therapist = Therapist.objects.create(
                medical_number=cd['therapist_medical_number'],
                first_name=cd['therapist_first_name'],
                last_name=cd['therapist_last_name']
            )
            request.session['current_therapist'] = new_therapist.id
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'therapist_login' in request.POST:
        therapist_form = TherapistForm(request.POST)
        if therapist_form.is_valid():
            cd = therapist_form.cleaned_data
            request.session['current_therapist'] = cd['therapist_id']
            return HttpResponseRedirect('/home/')
    if request.method == 'POST' and 'insurance_signup' in request.POST:
        #TODO:
        aadad = 1/0
    elif request.method == 'POST' and 'insurance_login' in request.POST:
        insurance_form = InsuranceForm(request.POST)
        if insurance_form.is_valid():
            cd = insurance_form.cleaned_data
            request.session['current_insurance'] = cd['insurance_id']
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'new_insurance' in request.POST:
        del request.session['current_insurance']
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
