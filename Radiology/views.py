# -*- coding: utf-8 -*-
from Radiology.forms import LoginForm, AppointmentForm, FactorForm, \
    MedicalHistoryForm
from Radiology.models import Insurance, Patient, Appointment, Doctor, Therapist, \
    Operation, Factor
from accounting import interface as accounting
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404


#TODO: alan dar majmoo 4 ta naghsh hast, yeki monshi, yeki operatore MRI, yeki AmadeSaz, yeki ham Pezeshk! ke ina
# har kodoom faghat ye esmo family daran
#Monshi ke bimaro paziresh mikone
#AmadeSaz forme pishineye pezeshkie bimaraye paziresh shode ro por mikone, zemnan operatore MRI e feli ro ham vared mikone
#operatore MRI hich gohi nemikhore, faghat inke alan ki sare dastgah vaisade mohemme
#Pezeshk ham hich gohi nemikhore ,faghat mibine ke kia barash paziresh shodan be tartib seda mizane bian too


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
def show_factor(request, id):
    factor = get_object_or_404(Factor, id=id)
    return HttpResponse('salam')


@login_required
def home(request):
    if request.method == "POST":
        form = FactorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #TODO: READ FROM SESSIOn
            print cd
            doctor = Doctor.objects.all()[0]
            cd['doctor_first_name'] = doctor.first_name
            cd['doctor_last_name'] = doctor.last_name
            cd['doctor_medical_number'] = doctor.medical_number
            cd['doctor_account_id'] = doctor.account_id
            factor = Factor.objects.create(**cd)
            return redirect(reverse(show_factor, args=(factor.id,)))
        else:
            print form.errors
    insurance_types = Insurance.objects.values_list('type', flat=True).distinct()
    operation_types = Operation.objects.values_list('type', flat=True).distinct()
    return render(request, 'home.html', {
        "insurance_types": insurance_types,
        "operation_types": operation_types,
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
def ajax_find_patients(request):
    if request.method != "POST":
        raise Http404()
    filters = {}
    if 'first_name' in request.POST:
        filters['first_name'] = request.POST['first_name']
    if 'last_name' in request.POST:
        filters['last_name'] = request.POST['last_name']
    if 'national_code' in request.POST:
        filters['national_code'] = request.POST['national_code']
    patients = Patient.objects.filter(**filters)
    print filters
    print patients
    return render(request, 'json/patients.json', {
        'patients': patients
    })

@login_required
def ajax_find_therapists(request):
    if request.method != "POST":
        raise Http404()
    filters = {}
    if 'first_name' in request.POST:
        filters['first_name'] = request.POST['first_name']
    if 'last_name' in request.POST:
        filters['last_name'] = request.POST['last_name']
    if 'medical_number' in request.POST:
        filters['medical_number'] = request.POST['medical_number']
    therapists = Therapist.objects.filter(**filters)
    return render(request, 'json/therapists.json', {'therapists':therapists})

@login_required
def ajax_find_insurances(request):
    if request.method != "POST":
        raise Http404()
    filters = {}
    if 'type' in request.POST:
        filters['type'] = request.POST['type']
    if 'category' in request.POST:
        filters['category'] = request.POST['category']
    if 'complementary' in request.POST:
        filters['complementary'] = request.POST['complementary']
    insurances = Insurance.objects.filter(**filters)
    if 'type' in filters:
        types = None
    else:
        types = insurances.values_list('type', flat=True).distinct()
    if 'category' in filters:
        categories = None
    else:
        categories = insurances.values_list('category', flat=True).distinct()
    if 'complementary' in filters:
        complementaries = None
    else:
        complementaries = insurances.values_list('complementary', flat=True).distinct()
    return render(request, 'json/insurances.json', {
        'types': types,
        'categories': categories,
        'complementaries': complementaries,
    })
    
@login_required
def ajax_find_operations(request):
    if request.method != "POST":
        raise Http404()
    filters = {}
    if 'type' in request.POST:
        filters['type'] = request.POST['type']
    if 'codeography' in request.POST:
        filters['codeography'] = request.POST['codeography']
    operations = Operation.objects.filter(**filters)
    if 'type' in filters:
        types = None
    else:
        types = operations.values_list('type', flat=True).distinct()
    if 'codeography' in request.POST:
        codeographies = None
    else:
        codeographies = operations.values_list('codeography', flat=True).distinct()
    return render(request, 'json/operations.json', {
        'types': types,
        'codeographies': codeographies,
    })

#TODO: inja bayad monshie tuye daftare pezeshk esme pezeshko login karde bashe
@login_required
def ajax_find_patients_list(request):
    if request.method != "POST":
        raise Http404()
    if 'doctor' in request.session:
        doctor_id = request.session['doctor']
        patients = Patient.objects.filter(patientturn__doctor__id=doctor_id).order_by("patientturn__turn")
    else:
        patients = None
    return render(request, 'json/patient_turn.json', {'patients':patients})
        

@login_required
def doctor_enroll(request):
    if request.method =="POST":
        if 'doctor_id' in request.POST:
            request.session['doctor'] = request.POST['doctor_id']
            return HttpResponseRedirect('/home/')
        else:
            return HttpResponseRedirect('/doctor_enroll/')
    return render(request, 'doctorEnroll.html', {'doctors':Doctor.objects.all()})

@login_required
def fill_medical_history(request):
    medical_history_form = None
    #FIXME:
    request.session['patient'] = 1
    if 'patient' in request.session:
        try:
            patient = Patient.objects.get(id=request.session['patient'])
            if patient.medical_history:
                medical_history_form = MedicalHistoryForm(instance=patient.medical_history)
        except Patient.DoesNotExist:
            del request.session['patient']
            #FIXME:
            return HttpResponseRedirect('/home/')
    return render(request,"medicalHistory.html", {'form':medical_history_form})