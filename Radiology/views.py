# -*- coding: utf-8 -*-
from Matab.decorators import *
from Radiology.forms import *
from Radiology.models import *
from accounting import interface as accounting
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404


#TODO: alan dar majmoo 4 ta naghsh hast, yeki monshi, yeki operatore MRI, yeki AmadeSaz, yeki ham Pezeshk! ke ina
# har kodoom faghat ye esmo family daran
#Monshi ke bimaro paziresh mikone
#AmadeSaz forme pishineye pezeshkie bimaraye paziresh shode ro por mikone, zemnan operatore MRI e feli ro ham vared mikone
#operatore MRI hich gohi nemikhore, faghat inke alan ki sare dastgah vaisade mohemme
#Pezeshk ham hich gohi nemikhore ,faghat mibine ke kia barash paziresh shodan be tartib seda mizane bian too


def login_view(request):
    if not request.user.is_anonymous():
        return redirect(logout_view)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            login(request, user)
            if user.is_staff:
                return  redirect(add_users)
            if user.usertype.type == UserType.RECEPTOR:
                return redirect(reception)
            return redirect(waiting_list)
    else:
        form = LoginForm()
    return render(request, "login.html", {
        'form': form,
    })


def logout_view(request):
    logout(request)
    return redirect(login_view)


@user_is_staff_or_404
def add_users(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password'])
            UserType.objects.create(type=cd['user_type'], user=user)
            return redirect(add_users)
    else:
        form = UserForm()
    return render(request, 'add_users.html', {
        "form": form,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t == UserType.RECEPTOR)
def reception(request):
    if request.method == "POST":
        form = FactorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #TODO: READ FROM SESSIOn
            doctor = Doctor.objects.get(id=request.session['doctor_id'])
            cd['doctor_first_name'] = doctor.first_name
            cd['doctor_last_name'] = doctor.last_name
            cd['doctor_medical_number'] = doctor.medical_number
            cd['doctor_account_id'] = doctor.account_id
            factor = Factor.objects.create(**cd)
            request.session['patient_id'] = Patient.objects.get(national_code=cd['patient_national_code']).id
            return redirect(show_factor, args=factor.id,)
        else:
            print form.errors
    insurance_types = Insurance.objects.values_list('type', flat=True).distinct()
    operation_types = Operation.objects.values_list('type', flat=True).distinct()
    return render(request, 'home.html', {
        "insurance_types": insurance_types,
        "operation_types": operation_types,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: Operation.objects.filter(type=t).count() > 0)
def waiting_list(request):
    pass



@user_logged_in
@user_type_conforms_or_404(lambda t: t == UserType.MRI)
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.waiting_list'))
def print_medical_history(request):
    pass


@user_logged_in
@user_type_conforms_or_404(lambda t: t == UserType.MRI)
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.waiting_list'))
def fill_medical_history(request):
    patient = Patient.objects.get(id=request.session['patient_id'])
    if request.method == "POST":
        if patient.medical_history:
            form = MedicalHistoryForm(request.POST, instance=patient.medical_history)
        else:
            form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            patient.medical_history = form.save()
            patient.save()
            return redirect(print_medical_history)
    else:
        if patient.medical_history:
            form = MedicalHistoryForm(instance=patient.medical_history)
        else:
            form = MedicalHistoryForm()
    return render(request, 'fill_medical_history.html', {
        'form': form,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t == UserType.MRI)
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.waiting_list'))
def print_mri_response_receipt(request):
    pass


@user_logged_in
@user_type_conforms_or_404(lambda t: Operation.objects.filter(type=t).count() > 0)
def sign_operator_in(request):
    pass


@user_logged_in
@user_type_conforms_or_404(lambda t: Operation.objects.filter(type=t).count() > 0)
def sign_operator_out(request):
    pass


@user_logged_in
@user_type_conforms_or_404(lambda t: Operation.objects.filter(type=t).count() > 0)
def write_response(request):
    pass


def appointment_day(request):
    return render(request, 'appointment_day.html', {})


def appointment(request, day):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        form.set_day(datetime.strptime(day, '%Y-%m-%d'))
        if form.is_valid():
            doctor = Doctor.objects.all()[0]
            app = Appointment.objects.create(
                patient=Patient.objects.get(id=request.session['patient_id']),
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


def ajax_find_insurances(request):
    if request.method != "POST":
        raise Http404()
    filters = {}
    if 'type' in request.POST:
        filters['type'] = request.POST['type']
    if 'category' in request.POST:
        filters['category'] = request.POST['category']
    if 'has_complementary' in request.POST:
        filters['has_complementary'] = request.POST['has_complementary']
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
    if 'has_complementary' in filters:
        has_complementaries = None
    else:
        has_complementaries = insurances.values_list('has_complementary', flat=True).distinct()
    if 'complementary' in filters:
        complementaries = None
    else:
        complementaries = insurances.values_list('complementary', flat=True).distinct()
    return render(request, 'json/insurances.json', {
        'types': types,
        'categories': categories,
        'has_complementaries': has_complementaries,
        'complementaries': complementaries,
    })
    

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


def ajax_find_patients_list(request):
    if request.method != "POST":
        raise Http404()
    #FIXME:
    patient_turns = PatientTurn.objects.filter(doctor__id=request.session['doctor_id']).order_by('turn')
    return render(request, 'json/patient_turn.json', {
        'patient_turns': patient_turns,
    })



def ajax_set_entered_patient(request):
    if request.method != "POST":
        raise Http404()
    patient_turn = get_object_or_404(PatientTurn, id=request.POST['id'])
    patient_turn.delete()
    return HttpResponse()


def register_patient(request):
    register_form = None
    if request.method == 'POST':
        register_form = RegisterPatientForm(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            Patient.objects.create(first_name=cd['first_name'], last_name=cd['last_name'],
                               national_code=cd['national_code'],
                               account_id=accounting.create_account(Patient.ACCOUNT_SERIES))
            return HttpResponseRedirect('/home/')
    else:
        register_form = RegisterPatientForm()
    return render(request, 'registerPatient.html', {'form':register_form})
    

def register_therapist(request):
    register_form = None
    if request.method == 'POST':
        register_form = RegisterTherapistForm(request.POST)
        if register_form.is_valid():
            cd = register_form.cleaned_data
            therapist = Therapist(first_name=cd['first_name'], last_name=cd['last_name'],
                               medical_number=cd['medical_number'])
            therapist.save()
            return HttpResponseRedirect('/home/')
    else:
        register_form = RegisterTherapistForm()
    return render(request, 'registerTherapist.html', {'form':register_form})