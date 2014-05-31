# -*- coding: utf-8 -*-
from Matab.decorators import *
from Radiology.forms import *
from Radiology.models import *
from accounting import interface as accounting
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models.sql.datastructures import Date
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
                #cloth.quantity -= 1
                cloth.get_good_from_store(1)
                cloth.save()
            if factor.operation_film_quantity != 0:
                film = Good.objects.get(name=factor.operation_film_name)
                #film.quantity -= factor.operation_film_quantity
                film.get_good_from_store(factor.operation_film_quantity)
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



def test_calendar(request):
    if request.method == "POST":
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse("selection: " + unicode(cd['start']) + " to " + unicode(cd['end']))
        else:
            print form.errors
    else:
        form = CalendarTestForm(request.POST)
    return render(request, 'calendar_test.html', {
        'form': form,
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
@exists_in_session_or_redirect('technician_id', reverse_lazy('Radiology.views.sign_technician_in'))
def waiting_list(request):
    turns = PatientTurn.objects.filter(type=request.user.usertype.operation).order_by("-turn")
    return render(request, 'waiting_list.html', {
        "turns": turns,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def accounting_page(request):
    return render(request, 'accounting.html')

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('personnel_id', reverse_lazy('Radiology.views.choose_personnel'))
def accounting_personnel(request):
    personnel = User.objects.get(id=request.session['personnel_id'])
    total_fee = 0
    factors = None
    operations = None
    factor_count = 0
    patient_count = 0
    if request.method == "POST":
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start']
            end_date = cd['end']
            factors = Factor.objects.filter((models.Q(technician_first_name=personnel.first_name, technician_last_name=personnel.last_name) 
                                             | models.Q(operator_first_name=personnel.first_name, operator_last_name=personnel.last_name) 
                                             | models.Q(receptor_first_name=personnel.first_name, receptor_last_name=personnel.last_name)),
                                            factor_date__gte=start_date,
                                            factor_date__lte=end_date
            ).distinct()
        else:
            print request.POST
            print form.errors
    else:
        form = CalendarTestForm()
    if factors:
        for factor in factors:
            total_fee += factor.total_fee
        codeographies = factors.values_list('operation_codeography', flat=True).distinct()
        operations = Operation.objects.filter(codeography__in=codeographies)
        factor_count = factors.count()
        patient_count = factors.values_list('patient_national_code', flat=True).distinct().count()
    return render(request, 'accounting_personnel.html', {
        'factors': factors,
        'form':form,
        'personnel':personnel,
        'total_fee':total_fee,
        'factor_count':factor_count,
        'patient_count':patient_count, 
        'operations':operations,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('insurance_id', reverse_lazy('Radiology.views.choose_insurance'))
def accounting_insurance(request):
    insurance = Insurance.objects.get(id=request.session['insurance_id'])
    factors = None
    start_date = None
    end_date = None
    if request.method == "POST":
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start']
            end_date = cd['end']
            factors = Factor.objects.filter(insurance_type=insurance.type,
                                            insurance_category=insurance.category,
                                            factor_date__gte=start_date,
                                            factor_date__lte=end_date,
                                            insurance_paid=False,
            ).distinct()
        else:
            print request.POST
            print form.errors
    else:
        form = CalendarTestForm()
    total_governmental_fee = 0
    total_share = 0
    factor_count = 0
    if factors:
        for factor in factors:
            total_share += factor.insurance_share
            total_governmental_fee += factor.operation_governmental_fee
            factor_count += 1
    return render(request, 'accounting_insurance.html', {
        'factors': factors,
        'form':form,
        'insurance':insurance,
        'total_governmental_fee':total_governmental_fee,
        'total_share': total_share,
        'factor_count': factor_count,
        'start_date': start_date,
        'end_date': end_date,
    })
    
@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('complementary_id', reverse_lazy('Radiology.views.choose_complementary'))
def accounting_complementary(request):
    complementary = ComplementaryInsurance.objects.get(id=request.session['complementary_id'])
    factors = None
    start_date = None
    end_date = None
    if request.method == "POST":
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start']
            end_date = cd['end']
            factors = Factor.objects.filter(insurance_complementary=complementary.type,
                                            factor_date__gte=start_date,
                                            factor_date__lte=end_date,
                                            complementary_paid=False,
            ).distinct()
        else:
            print request.POST
            print form.errors
    else:
        form = CalendarTestForm()
    total_governmental_fee = 0
    total_share = 0
    factor_count = 0
    if factors:
        for factor in factors:
            total_governmental_fee += factor.operation_governmental_fee
            total_share += factor.insurance_complementary_share
            factor_count += 1
    return render(request, 'accounting_complementary.html', {
        'factors': factors,
        'form':form,
        'complementary':complementary,
        'total_governmental_fee':total_governmental_fee,
        'total_share': total_share,
        'factor_count': factor_count,
        'start_date':start_date,
        'end_date': end_date,
    })
    
@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('therapist_id', reverse_lazy('Radiology.views.choose_therapist'))
def accounting_therapist(request):
    therapist = Therapist.objects.get(id=request.session['therapist_id'])
    factors = None
    if request.method == "POST":
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start']
            end_date = cd['end']
            factors = Factor.objects.filter(therapist_first_name=therapist.first_name,
                                            therapist_last_name=therapist.last_name,
                                            therapist_medical_number=therapist.medical_number,
                                            factor_date__gte=start_date,
                                            factor_date__lte=end_date
            ).distinct()
        else:
            print request.POST
            print form.errors
    else:
        form = CalendarTestForm()
    return render(request, 'accounting_therapist.html', {
        'factors': factors,
        'form':form,
        'therapist':therapist,
    })

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.choose_patient'))
def accounting_patient(request):
    patient = Patient.objects.get(id=request.session['patient_id'])
    total_debt = 0
    factors = None
    start_date = datetime.now()
    end_date = datetime.now()
    total_fee = 0
    total_paid = 0
    factor_count = 0
    if request.method == "POST":
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start']
            end_date = cd['end']
            factors = Factor.objects.filter(patient_first_name=patient.first_name,
                                            patient_last_name=patient.last_name,
                                            factor_date__gte=start_date,
                                            factor_date__lte=end_date
            )
        else:
            print request.POST
            print form.errors
    else:
        form = CalendarTestForm()
    if factors:
        for factor in factors:
            total_debt += factor.patient_debt_amount
            total_fee += factor.total_fee
            total_paid += factor.patient_paid_amount
            factor_count += 1
    return render(request, 'accounting_patient.html', {
        'factors': factors,
        'total_debt': total_debt,
        'form':form,
        'start_date':start_date,
        'end_date':end_date, 
        'total_debt':total_debt,
        'total_fee': total_fee,
        'total_paid':total_paid,
        'factor_count': factor_count,
    })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def choose_patient(request):
    if request.method == "POST":
        try:
            patient = Patient.objects.get(national_code=request.POST['national_code'],
                                          first_name=request.POST['first_name'],
                                          last_name=request.POST['last_name'])
            request.session['patient_id'] = patient.id
            return redirect(accounting_patient)
        except Patient.DoesNotExist:
            return redirect(choose_patient)
    return render(request, 'choose_patient.html')

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def choose_operation(request):
    if request.method == "POST":
        if 'operation_id' in request.POST:
            request.session['operation_id'] = request.POST['operation_id']
            return redirect(edit_operation)
        else:
            return redirect(choose_operation)
    else:
        operations = Operation.objects.all()
        return render(request, 'choose_operation.html', {
            'operations': operations,
        })

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def storing(request):
    goods = Good.objects.all()
    return render(request, 'storing.html', {
        'goods': goods,
    })


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
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def choose_personnel(request):
    if request.method == "POST":
        if 'personnel_id' in request.POST:
            request.session['personnel_id'] = request.POST['personnel_id']
            return redirect(accounting_personnel)
        else:
            return redirect(choose_personnel)
    else:
        personnel = User.objects.filter(is_staff=False)
        return render(request, 'choose_personnel.html', {
            'personnel': personnel,
        })

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def choose_therapist(request):
    if request.method == "POST":
        if 'therapist_id' in request.POST:
            request.session['therapist_id'] = request.POST['therapist_id']
            return redirect(accounting_therapist)
        else:
            return redirect(choose_therapist)
    else:
        therapists = Therapist.objects.all()
        return render(request, 'choose_therapist.html', {
            'therapists': therapists,
        })
        
        
@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def choose_insurance(request):
    if request.method == "POST":
        if 'insurance_id' in request.POST:
            request.session['insurance_id'] = request.POST['insurance_id']
            return redirect(accounting_insurance)
        else:
            return redirect(choose_insurance)
    else:
        insurances = Insurance.objects.all()
        return render(request, 'choose_insurance.html', {
            'insurances': insurances,
        })

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def choose_complementary(request):
    if request.method == "POST":
        if 'complementary_id' in request.POST:
            request.session['complementary_id'] = request.POST['complementary_id']
            return redirect(accounting_complementary)
        else:
            return redirect(choose_complementary)
    else:
        complementary = ComplementaryInsurance.objects.all()
        return render(request, 'choose_complementary.html', {
            'complementary': complementary,
        })


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def sign_technician_out(request):
    del request.session['technician_id']
    return redirect(sign_technician_in)


@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def write_response(request):
    pass


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def appointment(request):
    appointment_day = None 
    appointments = None
    if request.method == 'POST':
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            appointments = Appointment.objects.filter(day=cd['start'])
            request.session['appointment_day'] = cd['start']
        else:
            form = CalendarTestForm()
    elif 'appointment_day' in request.session:
        form = CalendarTestForm()
        appointments = Appointment.objects.filter(day=request.session['appointment_day'], visited=False)
    else:
        form = CalendarTestForm()
    return render(request, 'appointment.html', {
                'form':form,
                'appointments': appointments,
                'appointment_day': appointment_day
            })


@user_logged_in
def session_patient(request, id, next):
    turn = get_object_or_404(PatientTurn, id=id)
    request.session['patient_id'] = turn.patient.id
    turn.delete()
    return redirect(next)

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def session_appointment(request, id, next):
    pass

@user_logged_in
@exists_in_session_or_redirect("technician_id", reverse_lazy("Radiology.views.sign_technician_in"))
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['OPERATOR'])
def session_patient_and_set_factor(request, id, next):
    turn = get_object_or_404(PatientTurn, id=id)
    factor = turn.factor
    factor.operator_first_name = request.user.first_name
    factor.operator_last_name = request.user.last_name
    technician = Technician.objects.get(id=request.session['technician_id'])
    factor.technician_first_name = technician.first_name
    factor.technician_last_name = technician.last_name
    factor.save()
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
def ajax_find_good(request):
    if request.method != "POST":
        raise Http404()
    if 'id' in request.POST:
        try:
            good = Good.objects.get(id=request.POST['id'])
            request.session['good_id'] = good.id
            return render(request, 'json/good.json', {'good': good})
        except Good.DoesNotExist:
            #TODO:
            pass
    else:
        #TODO:
        pass


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
    if 'codeography' in request.POST:
        operations = Operation.objects.filter(codeography=request.POST['codeography'])
        count = operations.count()
        if count == 0:
            operation = None
        else:
            operation = operations[0]
        print render(request, 'json/operation.json', {
                    'count': count,
                    'operation':operation,
               })
        return render(request, 'json/operation.json', {
                    'count': count,
                    'operation':operation,
               })
    if 'type' in request.POST:
        filters['type'] = request.POST['type']
    if 'name' in request.POST:
        filters['name'] = request.POST['name']
    operations = Operation.objects.filter(**filters)
    print filters
    if 'type' in filters:
        types = None
    else:
        types = operations.values_list('type', flat=True).distinct()
    if 'name' in request.POST:
        names = None
    else:
        names = operations.values_list('name', flat=True).distinct()
    if 'codeography' in request.POST:
        codeographies = None
    else:
        print "Ey baba"
        codeographies = operations.values_list('codeography', flat=True).distinct()
        print codeographies
    return render(request, 'json/operations.json', {
        'types': types,
        'names': names,
        'codeographies':codeographies,
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
    if not factor.total_fee == 0:
        accounting.move_credit(factor.patient_account_id, accounting.get_static_account("office"),
                               factor.total_fee, "", "", "", datetime.now(), factor.id)
        factor.patient_paid = True
        factor.patient_paid_amount = factor.total_fee
    else:
        factor.patient_paid = True
        factor.patient_paid_amount = factor.total_fee
    factor.save()
    return render(request, 'json/patient_paid.json', {})

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_patient_pay_partial_factor(request):
    if request.method != "POST":
        raise Http404
    factor = get_object_or_404(Factor, id=request.POST['id'])
    pay_amount = float(request.POST['pay_amount'])
    #TODO: descriptions
    if factor.patient_paid:
        return render(request, 'json/error.json', {
            'errors': ['پرداخت شده است.'],
        })
    if factor.patient_debt_amount > pay_amount :
        accounting.move_credit(factor.patient_account_id, accounting.get_static_account("office"),
                               pay_amount, "", "", "", datetime.now(), factor.id)
        if factor.patient_debt_amount == pay_amount:
            factor.patient_paid = True
        factor.patient_paid_amount += pay_amount
        factor.patient_debt_amount -= pay_amount
    else:
        return render(request, 'json/error.json', {
                    'errors':['مبلغ پرداختی از بدهی بیشتر است']
                })
    factor.save()
    return render(request, 'json/patient_paid.json', {})

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_edit_good(request):
    if not request.method == "POST":
        raise Http404()
    if 'name' in request.POST:
        try:
            good = Good.objects.get(name=request.POST['name'])
            good.fee = request.POST['fee']
            good.quantity = request.POST['quantity']
            good.save()
            return render(request, 'json/good.json', {'good': good})
        except Good.DoesNotExist:
            pass
    else:
        pass

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_edit_patient(request):
    if not request.method == "POST":
        raise Http404()
    if 'id' in request.POST:
        try:
            patient = Patient.objects.get(id=request.POST['id'])
            patient.first_name = request.POST['first_name']
            patient.last_name = request.POST['last_name']
            patient.national_code = request.POST['national_code']
            #TODO: agar kode melli tekrari bood
            patient.save()
            return render(request, 'json/patient.json', {'patient': patient})
        except Patient.DoesNotExist:
            #TODO:
            print "Does Not Exist"
    else:
        #TODO:
        print "id nabood"

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_edit_operation(request):
    if not request.method == "POST":
        raise Http404()
    if 'id' in request.POST:
        try:
            operation = get_object_or_404(Operation, id=request.POST['id'])
            operation.type = request.POST['type']
            operation.name = request.POST['name']
            operation.codeography = request.POST['codeography']
            operation.film_id = int(request.POST['film'])
            operation.film_quantity = request.POST['film_quantity']
            operation.individual_fee = request.POST['individual_fee']
            operation.governmental_fee = request.POST['governmental_fee']
            operation.medical_fee = request.POST['medical_fee']
            #TODO: agar kode melli tekrari bood
            operation.save()
            return render(request, 'json/operation.json', {'operation': operation})
        except Patient.DoesNotExist:
            #TODO:
            print "Does Not Exist"
    else:
        #TODO:
        print "id nabood"

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_edit_therapist(request):
    if not request.method == "POST":
        raise Http404()
    if 'id' in request.POST:
        try:
            therapist = get_object_or_404(Therapist, id=request.POST['id'])
            therapist.first_name = request.POST['first_name']
            therapist.last_name = request.POST['last_name']
            therapist.medical_number = request.POST['medical_number']
            #TODO: agar nezam pezeshki
            therapist.save()
            return render(request, 'json/therapist.json', {'therapist': therapist})
        except Therapist.DoesNotExist:
            #TODO:
            return Http404()
    else:
        #TODO:
        return Http404()

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_edit_insurance(request):
    if not request.method == "POST":
        raise Http404()
    if 'id' in request.POST:
        try:
            insurance = get_object_or_404(Insurance, id=request.POST['id'])
            insurance.type = request.POST['type']
            insurance.category = request.POST['category']
            insurance.portion = request.POST['portion']
            #TODO: agar nezam pezeshki
            insurance.save()
            return render(request, 'json/insurance.json', {'insurance': insurance})
        except Insurance.DoesNotExist:
            #TODO:
            return Http404()
    else:
        #TODO:
        return Http404()

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def ajax_edit_complementary(request):
    if not request.method == "POST":
        raise Http404()
    if 'id' in request.POST:
        try:
            complementary = get_object_or_404(ComplementaryInsurance, id=request.POST['id'])
            complementary.type = request.POST['type']
            #TODO: agar nezam pezeshki
            complementary.save()
            return render(request, 'json/complementary_insurance.json', {'complementary': complementary})
        except ComplementaryInsurance.DoesNotExist:
            #TODO:
            return Http404()
    else:
        #TODO:
        return Http404()



@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def add_good_to_store(request):
    if not request.method == "POST":
        raise Http404()
    try:
        good = Good.objects.get(name=request.POST['name'])
        good.add_good_to_store(int(request.POST['quantity']))
       # good.quantity = good.quantity + int(request.POST['quantity'])
        good.save()
        return render(request, 'json/good.json')
    except Good.DoesNotExist:
        #TODO:
        return render(request, 'json/error.json')


@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def register_good(request):
    if not request.method == "POST":
        raise Http404()
    form = GoodForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        good = Good.objects.create(**cd)
        return render(request, 'json/good.json', {'good': good})
    return render(request, 'json/error.json', {'errors': form.errors})

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('appointment_day', reverse_lazy("Radiology.views.appointment"))
def register_appointment(request):
    if not request.method == "POST":
        raise Http404()
    form = AppointmentForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cd['day'] = request.session['appointment_day']
        appointment = Appointment.objects.create(**cd)
        return render(request, 'json/appointment.json', {
                    'appointment': appointment,
                })
    else :
        print form.errors
    return render(request, 'json/error.json',{
                'errors': form.errors,
            })


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
        return render(request, 'json/operation.json', {
            'operation': operation,
        })
        
  
  
        
@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def edit(request):
    return render(request, 'edit.html')

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('patient_id', reverse_lazy('Radiology.views.choose_patient'))
def edit_patient(request):
    patient = get_object_or_404(Patient,id=request.session['patient_id'])
    return render(request, 'edit_patient.html', {'patient':patient})

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('therapist_id', reverse_lazy('Radiology.views.choose_therapist'))
def edit_therapist(request):
    therapist = get_object_or_404(Therapist, id=request.session['therapist_id'])
    return render(request, 'edit_therapist.html', {'therapist':therapist})

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
def edit_personnel(request):
    return render(request, 'edit.html')

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('insurance_id', reverse_lazy('Radiology.views.choose_insurance'))
def edit_insurance(request):
    insurance = get_object_or_404(Insurance, id=request.session['insurance_id'])
    return render(request, 'edit_insurance.html', {'insurance':insurance})

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('complementary_id', reverse_lazy('Radiology.views.choose_complementary'))
def edit_complementary(request):
    complementary = get_object_or_404(ComplementaryInsurance, id=request.session['complementary_id'])
    return render(request, 'edit_complementary.html', {'complementary':complementary})

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('operation_id', reverse_lazy('Radiology.views.choose_operation'))
def edit_operation(request):
    operation = get_object_or_404(Operation, id=request.session['operation_id'])
    film_types = Good.objects.all()
    return render(request, 'edit_operation.html', {'operation':operation,
                                                   'film_types':film_types,
                                                   'film':operation.film,
                                                   })

@user_logged_in
@user_type_conforms_or_404(lambda t: t.type == UserType.TYPES['RECEPTOR'])
@exists_in_session_or_redirect('good_id', reverse_lazy('Radiology.views.storing'))
def storing_detailed(request):
    good = Good.objects.get(id=request.session['good_id'])
    factors = None
    start_date = None
    end_date = None
    if request.method == "POST":
        form = CalendarTestForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start']
            end_date = cd['end']
            end_date += timedelta(days=1, )
            factors = GoodFactor.objects.filter(good_id=good.id,
                                            date__gte=start_date,
                                            date__lte=end_date,
            ).distinct()
        else:
            print request.POST
            print form.errors
    else:
        form = CalendarTestForm()
    return render(request, 'storing_detailed.html', {
        'factors': factors,
        'form':form,
        'good':good,
        'start_date': start_date,
        'end_date': end_date,
    })