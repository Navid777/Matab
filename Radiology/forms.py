# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Radiology.models import Patient, Appointment, Therapist, Insurance, \
    Operation, MedicalHistory, UserType, Good, ComplementaryInsurance
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q
from django.utils.datetime_safe import date


username_label = "نامِ کاربری"
password_label = "گذرواژه"
first_name_error = "لطفا نامِ بیمار را وارد کنید."
last_name_error = "لطفا نامِ خانوادگیِ بیمار را وارد کنید."
national_code_error = "لطفا کدِ ملیِ بیمار را وارد کنید."
national_code_duplicate_error = "این کدِ ملی قبلا استفاده شده است. "
invalid_patient_error = "اطلاعاتِ واردشده صحیح نیست."
not_complete_error = "اطلاعاتِ واردشده کامل نیست."
overlapping_appointments_error = "وقت مشخص شده خالی نیست."
therapist_first_name_error = "لطفا نام پزشک معالج را وارد کنید."
therapist_last_name_error = "لطفا نام خانوادگی پزشک معالج را وارد کنید."
therapist_medical_duplicate_error = "این شماره نظام پزشکی قبلا استفاده شده است."


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username'}), label=username_label)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'username'}), label=password_label)

    def __unicode__(self):
        return self.username

    def clean_username(self):
        username = self.cleaned_data['username']
        if not User.objects.filter(username=username):
            raise forms.ValidationError("No such user.")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password:
            raise forms.ValidationError("Enter a password.")
        return password

    def clean(self):
        cd = super(LoginForm, self).clean()
        username = cd.get('username')
        password = cd.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                pass
            else:
                raise forms.ValidationError('User is not active.')
        else:
            raise forms.ValidationError('Username/Password invalid.')

        return cd


class UserForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=50)
    username = forms.SlugField(max_length=20)
    password = forms.CharField(max_length=20)
    email = forms.EmailField(required=False)
    user_type = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user_type'].choices = \
            [(v, "اپراتور" + " " + v)
             for v in Operation.objects.values_list('type', flat=True).distinct()] + \
            [(UserType.TYPES['RECEPTOR'], UserType.TYPES['RECEPTOR'])]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError('Username already exists')
        return username

    def clean(self):
        cd = super(UserForm, self).clean()
        user_type = cd.get('user_type')
        if user_type == UserType.TYPES['RECEPTOR']:
            cd['user_operation'] = None
        else:
            cd['user_operation'] = user_type
            cd['user_type'] = UserType.TYPES['OPERATOR']
        return cd


class AppointmentForm(forms.Form):
    first_name = forms.CharField(max_length = 30)
    last_name = forms.CharField(max_length = 30)
    national_code = forms.CharField(max_length = 30, required=False)
    start_time = forms.TimeField()
    day = forms.DateField(required=False)


class FactorForm(forms.Form):
    patient_first_name = forms.CharField(max_length=30)
    patient_last_name = forms.CharField(max_length=50)
    patient_national_code = forms.CharField(max_length=30)
    patient_paid_amount = forms.FloatField(required=False)
    #patient_account_id = forms.IntegerField()
    #doctor_first_name = forms.CharField(max_length=30)
    #doctor_last_name = forms.CharField(max_length=50)
    #doctor_medical_number = forms.CharField(max_length=20)
    #doctor_account_id = forms.IntegerField()
    therapist_first_name = forms.CharField(max_length=30)
    therapist_last_name = forms.CharField(max_length=50)
    therapist_medical_number = forms.CharField(max_length=20)
    operation_id = forms.IntegerField()
    #operation_type = forms.CharField(max_length=30)
    #operation_name = forms.CharField(max_length=30)
    #operation_codeography = forms.CharField(max_length=30)
    operation_cloth = forms.BooleanField(required=False)
    #operation_fee = forms.FloatField()
    insurance_type = forms.CharField(max_length=100)
    insurance_category = forms.CharField(max_length=100)
    insurance_has_complementary = forms.BooleanField(required=False)
    insurance_complementary = forms.CharField(max_length=100, required=False)
    #insurance_portion = forms.IntegerField()
    insurance_serial = forms.CharField(max_length=20)
    insurance_page = forms.CharField(max_length=20)
    therapist_visit_date = forms.DateField(required=False)
    comment = forms.CharField(max_length=300, required=False)
    insurance_exp_date = forms.DateField()
    discount = forms.FloatField(required=False)
    #insurance_account_id = forms.IntegerField()
    #insurance_complementary_account_id = forms.IntegerField()
    #total_fee = forms.FloatField()
    #patient_share = forms.FloatField()

    def clean(self):
        super(FactorForm, self).clean()
        cd = self.cleaned_data
        cd['patient_paid_amount'] = 0
        
        #Patient information
        try:
            cd['patient_account_id'] = Patient.objects.get(
                first_name=cd.get('patient_first_name'),
                last_name=cd.get('patient_last_name'),
                national_code=cd.get('patient_national_code')).account_id
        except Patient.DoesNotExist:
            raise ValidationError('Invalid Patient')
        
        #Operation information
        try:
            operation = Operation.objects.get(
                id=cd.get('operation_id'),
                )
            cd['operation_type'] = operation.type
            cd['operation_codeography'] = operation.codeography
            cd['operation_name'] = operation.name
            cd['operation_governmental_fee'] = operation.governmental_fee
            cd['operation_individual_fee'] = operation.individual_fee
            cd['operation_medical_fee'] = operation.medical_fee
            if operation.film:
                cd['operation_film_name'] = Good.objects.get(id=operation.film_id).name
                cd['operation_film_fee'] = Good.objects.get(id=operation.film_id).fee
                cd['operation_film_quantity'] = operation.film_quantity
            else:
                cd['operation_film_fee'] = 0
        except Operation.DoesNotExist:
            raise ValidationError('Invalid operation')
        except Good.DoesNotExist:
            raise ValidationError('Invalid film type')  
        if cd['operation_cloth']:
            cd['operation_cloth_fee'] = Good.objects.get(name=Good.CLOTH).fee
        else:
            cd['operation_cloth_fee'] = 0
        
        #Insurance information
        try:
            insurance = Insurance.objects.get(
                type=cd.get('insurance_type'),
                category=cd.get('insurance_category'),
            )
            cd['insurance_portion'] = insurance.portion
            cd['insurance_account_id'] = insurance.account_id
            if cd['insurance_has_complementary']:
                cd['insurance_complementary_account_id'] = ComplementaryInsurance.objects.get(
                    type=cd['insurance_complementary']
                ).account_id
        except Insurance.DoesNotExist:
            raise ValidationError('Invalid insurance')
        except ComplementaryInsurance.DoesNotExist:
            raise ValidationError('Invalid complementary insurance')
        
        #Payment information
        if cd['insurance_has_complementary']:
            patient_share = 0
            insurance_share = cd['operation_governmental_fee'] * insurance.portion / 100
            complementary_share = cd['operation_governmental_fee'] - insurance_share
        else:
            insurance_share = cd['operation_governmental_fee'] * insurance.portion / 100
            patient_share = cd['operation_individual_fee'] - insurance_share
            complementary_share = 0
            cd['complementary_paid'] = True
        cd['patient_share'] = patient_share
        cd['insurance_share'] = insurance_share
        cd['insurance_complementary_share'] = complementary_share
        cd['patient_payable'] = patient_share + cd['operation_cloth_fee'] + cd['operation_film_fee']
            
        #Date information
        cd['factor_date'] = date.today()
        
        
        return cd

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory


class GoodForm(forms.Form):
    name = forms.CharField(max_length=30)
    fee = forms.FloatField()
    quantity = forms.IntegerField()

    def clean_name(self):
        name = self.cleaned_data['name']
        if Good.objects.filter(name=name):
            raise ValidationError("Good already exists.")
        return name


class PatientForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    national_code = forms.CharField(max_length=30)

    def clean_national_code(self):
        national_code = self.cleaned_data['national_code']
        if Patient.objects.filter(national_code=national_code):
            raise ValidationError(national_code_duplicate_error)
        return national_code


class InsuranceForm(forms.Form):
    type = forms.CharField(max_length=100)
    category = forms.CharField(max_length=100)
    portion = forms.IntegerField()

    def clean(self):
        super(InsuranceForm, self).clean()
        cd = self.cleaned_data
        if Insurance.objects.filter(
                type=cd.get('type'),
                category=cd.get('category'), ):
            raise ValidationError('بیمه تکراری است.')
        return cd


class ComplementaryInsuranceForm(forms.Form):
    type = forms.CharField(max_length=100)


class TherapistForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    medical_number = forms.CharField(max_length=20)

    def clean_medical_number(self):
        medical_number = self.cleaned_data['medical_number']
        if Therapist.objects.filter(medical_number=medical_number):
            raise ValidationError(therapist_medical_duplicate_error)
        return medical_number


class OperationForm(forms.Form):
    type = forms.CharField(max_length=30)
    name = forms.CharField(max_length=30)
    codeography = forms.IntegerField()
    individual_fee = forms.FloatField()
    governmental_fee = forms.FloatField()
    medical_fee = forms.FloatField()
    film_id = forms.IntegerField(required=False)
    film_quantity = forms.IntegerField(required=False)


class CalendarTestForm(forms.Form):
    start = forms.DateField(required=False)
    end = forms.DateField(required=False)