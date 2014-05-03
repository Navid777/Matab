# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Radiology.models import Patient, Appointment, Therapist, Insurance, \
    Operation, MedicalHistory, UserType
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.query_utils import Q


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
            [(UserType.RECEPTOR, UserType.RECEPTOR)]

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError('Username already exists')
        return username


class AppointmentForm(forms.Form):
    start_time = forms.TimeField()
    end_time = forms.TimeField()

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.day = None

    def set_day(self, day):
        self.day = day

    def clean(self):
        cd = super(AppointmentForm, self).clean()
        st = cd['start_time']
        et = cd['end_time']
        if Appointment.objects.filter(day=self.day).filter(Q(start_time__lt=st, end_time__gt=st)
                                            | Q(start_time__lt=et, end_time__gt=et)).count() > 0:
            raise forms.ValidationError(overlapping_appointments_error)
        print cd
        return cd


class FactorForm(forms.Form):
    patient_first_name = forms.CharField(max_length=30)
    patient_last_name = forms.CharField(max_length=50)
    patient_national_code = forms.CharField(max_length=30)
    #patient_account_id = forms.IntegerField()
    #doctor_first_name = forms.CharField(max_length=30)
    #doctor_last_name = forms.CharField(max_length=50)
    #doctor_medical_number = forms.CharField(max_length=20)
    #doctor_account_id = forms.IntegerField()
    therapist_first_name = forms.CharField(max_length=30)
    therapist_last_name = forms.CharField(max_length=50)
    therapist_medical_number = forms.CharField(max_length=20)
    operation_type = forms.CharField(max_length=30)
    operation_codeography = forms.CharField(max_length=30)
    operation_cloth = forms.BooleanField()
    #operation_fee = forms.FloatField()
    insurance_type = forms.CharField(max_length=100)
    insurance_category = forms.CharField(max_length=100)
    insurance_has_complementary = forms.BooleanField(required=False)
    insurance_complementary = forms.CharField(max_length=100, required=False)
    #insurance_portion = forms.IntegerField()
    insurance_serial = forms.CharField(max_length=20)
    insurance_page = forms.CharField(max_length=20)
    #insurance_account_id = forms.IntegerField()
    #insurance_complementary_account_id = forms.IntegerField()
    #total_fee = forms.FloatField()
    #patient_share = forms.FloatField()

    def clean(self):
        super(FactorForm, self).clean()
        cd = self.cleaned_data
        try:
            cd['patient_account_id'] = Patient.objects.get(
                first_name=cd.get('patient_first_name'),
                last_name=cd.get('patient_last_name'),
                national_code=cd.get('patient_national_code')).account_id
        except Patient.DoesNotExist:
            raise ValidationError('اطلاعات بیمار نادرست است')
        try:
            cd['operation_fee'] = Operation.objects.get(
                type=cd.get('operation_type'),
                codeography=cd.get('operation_codeography'),
            ).fee
        except Operation.DoesNotExist:
            raise ValidationError('خدمت نادرست است')
        try:
            insurance = Insurance.objects.get(
                type=cd.get('insurance_type'),
                category=cd.get('insurance_category'),
                has_complementary=cd.get('insurance_has_complementary'),
                complementary=cd.get('insurance_complementary')
            )
            cd['insurance_portion'] = insurance.portion
            cd['insurance_account_id'] = insurance.account_id
            if insurance.has_complementary:
                cd['insurance_complementary_account_id'] = insurance.complementary_account_id
        except Insurance.DoesNotExist:
            raise ValidationError('بیمه نادرست است')
        cd['total_fee'] = 1000
        cd['patient_share'] = 973
        return cd


class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory


class RegisterPatientForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    national_code = forms.CharField(max_length=30)

    def clean_national_code(self):
        national_code = self.cleaned_data['national_code']
        if Patient.objects.filter(national_code=national_code):
            raise ValidationError(national_code_duplicate_error)
        return national_code


class RegisterTherapistForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    medical_number = forms.CharField(max_length=20)

    def clean_medical_number(self):
        medical_number = self.cleaned_data['medical_number']
        if Therapist.objects.filter(medical_number=medical_number):
            raise ValidationError(therapist_medical_duplicate_error)
        return medical_number