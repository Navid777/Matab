# -*- coding: utf-8 -*-
from Radiology.forms import LoginForm, PatientForm
from Radiology.models import Patient
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
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
    if request.method == 'POST' and 'sabt' in request.POST:
        patient_form = PatientForm(request.POST)
        if patient_form.is_valid():
            print patient_form
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
        if patient_form.is_valid():
            cd = patient_form.cleaned_data
            request.session['current_patient'] = cd['patient_id']
            return HttpResponseRedirect('/home/')
    elif request.method == 'POST' and 'jadid' in request.POST:
        del request.session['current_patient']
        return HttpResponseRedirect('/home/')
    else:
        if not 'current_patient' in request.session:
            patient_form = PatientForm()
        else:
            has_patient = True
            try:
                patient = Patient.objects.get(id=request.session['current_patient'])
                return render(request, 'home.html', {'has_patient': has_patient, 'patient': patient})
            except Patient.DoesNotExist:
                del request.session['current_patient']
                HttpResponseRedirect('/home/')
    return render(request, 'home.html', {'patient_form': patient_form})


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')