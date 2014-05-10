# -*- coding: utf-8 -*-
from Matab.decorators import *
from Radiology.forms import *
from Radiology.models import *
from accounting import interface as accounting
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
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
                return redirect(add_users)
            if user.usertype.type == UserType.TYPES['RECEPTOR']:
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
            UserType.objects.create(type=cd['user_type'], operation=cd['user_operation'], user=user)
            return redirect(add_users)
    else:
        form = UserForm()
    return render(request, 'add_users.html', {
        "form": form,
    })


#todo: etelaate bimare voroodi dar forme registere bimar neshan dade shavad
#vaghti shomare nezam pezeshki zade shod va dorost bood beppare tuye entekhabe khedmat
#bime takmili khodesh kelase jodast
#name monshi o operator o amadesaz be factor ezafe shavad
#saate kari mohem nist
#khedmat 3 ta gheimat dare!    
@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def reception(request):
    if request.method == "POST":
        form = FactorForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cd['receptor_first_name'] = request.user.first_name
            cd['receptor_last_name'] = request.user.last_name
            factor = Factor.objects.create(**cd)
            if factor.operation_cloth:
                cloth = Good.objects.get(name='لباس')
                cloth.quantity = cloth.quantity - 1
                cloth.save()
            if factor.operation_film_quantity != 0 :
                film = Good.objects.get(name=factor.operation_film_name)
                film.quantity = film.quantity - factor.operation_film_quantity
                film.save()
            patient = factor.get_patient()
            request.session['patient_id'] = patient.id
            PatientTurn.objects.create(
                patient=patient,
                type=factor.operation_type,
                turn=datetime.now(),
                factor_id=factor.id,
            )
            return redirect(reverse(show_factor, args=(factor.id,)))
        else:
            print form.errors
    insurance_types = Insurance.objects.values_list('type', flat=True).distinct()
    operation_types = Operation.objects.values_list('type', flat=True).distinct()
    complementary_insurance_types = ComplementaryInsurance.objects.values_list('type', flat=True).distinct()
    #TODO: faghat betavanad az film ha entekhab konad
    film_types = Good.objects.all()
    return render(request, 'reception.html', {
        "insurance_types": insurance_types,
        "operation_types": operation_types,
        "film_types": film_types,
        "complementary_insurance_types": complementary_insurance_types,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def show_factor(request, id):
    factor = get_object_or_404(Factor, id=id)
    return render(request, "show_factor.html", {
        'factor': factor,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('patient_id', 'reverse_lazy("Radiology.views.reception")')
def show_unpaid_factors(request):
    try:
        patient = Patient.objects.get(id=request.session['patient_id'])
        factors = Factor.objects.filter(
            patient_first_name=patient.first_name,
            patient_last_name=patient.last_name,
            patient_national_code=patient.national_code,
            patient_paid=False,
        )
    except Patient.DoesNotExist:
        return redirect(reception)
    return render(request, 'show_unpaid_factors.html', {
        'factors': factors,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def waiting_list(request):
    turns = PatientTurn.objects.filter(type=request.user.usertype.operation).order_by("-turn")
    return render(request, 'waiting_list.html', {
        "turns": turns,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def accounting(request):
    return render(request, 'accounting.html')

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.log_patient_in'))
def patient_accounting(request):
    pass

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def storing(request):
    return render(request, 'storing.html')

@user_logged_in
@user_type_conforms_or_404(lambda t: t.operation == UserType.MRI_OPERATION)
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.waiting_list'))
def print_medical_history(request):
    try:
        patient = Patient.objects.get(id=request.session['patient_id'])
        try:
            medical_history = patient.medical_history
            return render(request, "print_medical_history.html", {
                'medical_history': medical_history,
                'patient': patient,
            })
        except MedicalHistory.DoesNotExist:
            return redirect(fill_medical_history)
    except Patient.DoesNotExist:
        return redirect(waiting_list)


@user_logged_in
@user_type_conforms_or_404(lambda t: t.operation == UserType.MRI_OPERATION)
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
@user_type_conforms_or_404(lambda t: t.operation == UserType.MRI_OPERATION)
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.waiting_list'))
def print_mri_response_receipt(request):
    pass


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def sign_technician_in(request):
    if request.method == "POST":
        if 'technician_id' in request.POST:
            request.session['technician_id'] = request.POST['technician_id']
            return redirect(waiting_list)
        else:
            return redirect(sign_technician_in)
    else:
        technicians = Technician.objects.filter(operation=request.user.usertype.operation)
        return render(request, 'sign_technician_in.html', {
            'technicians': technicians,
        })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def sign_technician_out(request):
    del request.session['technician_id']
    return redirect(sign_technician_in)


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def write_response(request):
    pass


def appointment_day(request):
    return render(request, 'appointment_day.html', {})


def appointment(request, day):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        form.set_day(datetime.strptime(day, '%Y-%m-%d'))
        if form.is_valid():
            app = Appointment.objects.create(
                patient=Patient.objects.get(id=request.session['patient_id']),
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


@user_logged_in
def session_patient(request, id, next):
    turn = get_object_or_404(PatientTurn, id=id)
    request.session['patient_id'] = turn.patient.id
    turn.delete()
    return redirect(next)


@user_logged_in
def session_clear_patient(request):
    del request.session['patient_id']
    #TODO: redirect where?
    return redirect(waiting_list)


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
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


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
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
    return render(request, 'json/therapists.json', {'therapists': therapists})


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_find_insurances(request):
    if request.method != "POST":
        raise Http404()
    filters = {}
    if 'type' in request.POST:
        filters['type'] = request.POST['type']
    if 'category' in request.POST:
        filters['category'] = request.POST['category']
    insurances = Insurance.objects.filter(**filters)
    if 'type' in filters:
        types = None
    else:
        types = insurances.values_list('type', flat=True).distinct()
    if 'category' in filters:
        categories = None
    else:
        categories = insurances.values_list('category', flat=True).distinct()
    return render(request, 'json/insurances.json', {
        'types': types,
        'categories': categories,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
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


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def ajax_find_patients_list(request):
    if request.method != "POST":
        raise Http404()
        #FIXME:
    turns = PatientTurn.objects.filter(type=request.user.usertype.operation).order_by("-turn")
    return render(request, 'json/patient_turn.json', {
        'turns': turns,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_patient_pay_factor(request):
    if request.method != "POST":
        raise Http404
    factor = get_object_or_404(Factor, id=request.POST['id'])
    #TODO: descriptions
    if factor.patient_paid:
        return render(request, 'json/error.json', {
            'errors': ['پرداخت شده است.'],
        })
    if not factor.insurance_has_complementary:
        accounting.move_credit(factor.patient_account_id, accounting.get_static_account("office"),
                               factor.patient_share, "", "", "", datetime.now(), factor.id)
        factor.patient_paid = True
        factor.save()
    return render(request, 'json/patient_paid.json', {})


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def register_patient(request):
    if not request.method == "POST":
        raise Http404()
    form = PatientForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cd['account_id'] = accounting.create_account(Patient.ACCOUNT_SERIES)
        patient = Patient.objects.create(**cd)
        return render(request, 'json/patient.json', {
            'patient': patient,
        })
    return render(request, 'json/error.json', {
        'errors': form.errors,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def register_therapist(request):
    if not request.method == "POST":
        raise Http404()
    form = TherapistForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        therapist = Therapist.objects.create(**cd)
        return render(request, 'json/therapist.json', {
            'therapist': therapist,
        })
    return render(request, 'json/error.json', {
        'errors': form.errors,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def register_insurance(request):
    if not request.method == "POST":
        raise Http404()
    form = InsuranceForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cd['account_id'] = accounting.create_account(Insurance.ACCOUNT_SERIES)
        insurance = Insurance.objects.create(**cd)
        return render(request, 'json/insurance.json', {
            'insurance': insurance,
        })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def register_complementary_insurance(request):
    if not request.method == "POST":
        raise Http404()
    form = ComplementaryInsuranceForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cd['account_id'] = accounting.create_account(ComplementaryInsurance.ACCOUNT_SERIES)
        complementary_insurance = ComplementaryInsurance.objects.create(**cd)
        return render(request, 'json/complementary_insurance.json', {
            'complementary_insurance': complementary_insurance,
        })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def register_operation(request):
    if not request.method == "POST":
        raise Http404()
    form = OperationForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        operation = Operation.objects.create(**cd)
        return render(request, 'json/insurance.json', {
            'operation': operation,
        })