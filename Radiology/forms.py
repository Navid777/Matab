# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from Radiology.models import Patient, Appointment, Therapist, Insurance, \
    Operation
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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


class PatientForm(forms.Form):
    patient_id = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'patient_id'}))
    patient_first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'patient_first_name'}))
    patient_last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'patient_last_name'}))
    patient_national_code = forms.IntegerField(required=False,
                                               widget=forms.TextInput(attrs={'class': 'patient_national_code'}))

    def clean(self):
        cd = super(PatientForm, self).clean()
        if 'patient_login' in self.data:
            patient_id = cd.get('patient_id')
            first_name = cd.get('patient_first_name')
            last_name = cd.get('patient_last_name')
            national_code = cd.get('patient_national_code')
            if patient_id is not None:
                patients = Patient.objects.filter(id=patient_id)
                if not patients:
                    raise forms.ValidationError(invalid_patient_error)
            elif national_code is not None:
                patients = Patient.objects.filter(national_code=national_code)
                if patients.count() == 1:
                    cd['patient_id'] = patients[0].id
                else:
                    raise forms.ValidationError(invalid_patient_error)
            elif last_name:
                if first_name:
                    patients = Patient.objects.filter(first_name=first_name, last_name=last_name)
                    print patients
                    if patients.count() == 1:
                        cd['patient_id'] = patients[0].id
                    else:
                        raise forms.ValidationError(not_complete_error)
                else:
                    patients = Patient.objects.filter(last_name=last_name)
                    if patients.count() == 1:
                        cd['patient_id'] = patients[0].id
                    else:
                        raise forms.ValidationError(not_complete_error)
            elif first_name:
                patients = Patient.objects.filter(first_name=first_name)
                if patients.count() == 1:
                    cd['patient_id'] = patients[0].id
                else:
                    raise forms.ValidationError(not_complete_error)
            else:
                raise forms.ValidationError(not_complete_error)
        return cd

    def clean_patient_id(self):
        patient_id = self.cleaned_data['patient_id']
        return patient_id

    def clean_patient_first_name(self):
        patient_first_name = self.cleaned_data['patient_first_name']
        if 'patient_signup' in self.data:
            if not patient_first_name:
                raise forms.ValidationError(first_name_error)
        return patient_first_name

    def clean_patient_last_name(self):
        patient_last_name = self.cleaned_data['patient_last_name']
        if 'patient_signup' in self.data:
            if not patient_last_name:
                raise forms.ValidationError(last_name_error)
        return patient_last_name

    def clean_patient_national_code(self):
        patient_national_code = self.cleaned_data['patient_national_code']
        if 'patient_signup' in self.data:
            if not patient_national_code:
                raise forms.ValidationError(national_code_error)
            if Patient.objects.filter(national_code=patient_national_code):
                raise forms.ValidationError(national_code_duplicate_error)
        return patient_national_code


class InsuranceForm(forms.Form):
    BOOLEAN_CHOICES = (
            ('False', 'ندارد'),
            ('True', 'دارد')
    )
    insurance_type = forms.ModelChoiceField(queryset=Insurance.objects.all(), to_field_name="insurance_type")
    insurance_category = forms.ModelChoiceField(queryset=Insurance.objects.all(),to_field_name="insurance_category")
    complementary_insurance = forms.ChoiceField(choices=BOOLEAN_CHOICES)
    insurance_serial = forms.IntegerField()
    insurance_page_num = forms.IntegerField()


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
    

class TherapistForm(forms.Form):
    therapist_medical_number = forms.IntegerField(required=False)
    therapist_first_name = forms.CharField(required=False)
    therapist_last_name = forms.CharField(required=False)
    therapist_visit_date = forms.DateField(required=False,widget=forms.DateTimeInput) 

    def clean_therapist_first_name(self):
        therapist_first_name = self.cleaned_data['therapist_first_name']
        if 'therapist_signup' in self.data:
            if not therapist_first_name:
                raise forms.ValidationError(therapist_first_name_error)
        return therapist_first_name
    
    def clean_therapist_last_name(self):
        therapist_last_name = self.cleaned_data['therapist_last_name']
        if 'therapist_signup' in self.data:
            if not therapist_last_name:
                raise forms.ValidationError(therapist_last_name_error)
        return therapist_last_name
    def clean_therapist_medical_number(self):
        therapist_medical_number = self.cleaned_data['therapist_medical_number']
        if 'therapist_signup' in self.data:
            if Therapist.objects.filter(medical_number=therapist_medical_number):
                raise forms.ValidationError(therapist_medical_duplicate_error)
        return therapist_medical_number
    
    def clean(self):
        cd = super(TherapistForm, self).clean()
        if 'therapist_login' in self.data:
            first_name = cd.get('therapist_first_name')
            last_name = cd.get('therapist_last_name')
            medical_number = cd.get('therapist_medical_number')
            if medical_number is not None:
                therapists = Therapist.objects.filter(medical_number=medical_number)
                if therapists.count() == 1:
                    cd['therapist_id'] = therapists[0].id
                else:
                    raise forms.ValidationError(invalid_patient_error)
            elif last_name:
                if first_name:
                    therapists = Therapist.objects.filter(first_name=first_name, last_name=last_name)
                    if therapists.count() == 1:
                        cd['therapist_id'] = therapists[0].id
                    else:
                        raise forms.ValidationError(not_complete_error)
                else:
                    therapists = Therapist.objects.filter(last_name=last_name)
                    if therapists.count() == 1:
                        cd['therapist_id'] = therapists[0].id
                    else:
                        raise forms.ValidationError(not_complete_error)
            elif first_name:
                therapists = Therapist.objects.filter(first_name=first_name)
                if therapists.count() == 1:
                    cd['therapist_id'] = therapists[0].id
                else:
                    raise forms.ValidationError(not_complete_error)
            else:
                raise forms.ValidationError(not_complete_error)
        return cd

    
class OperationForm(forms.Form):
    operation_type = forms.ModelChoiceField(queryset=Operation.objects.all())
    operation_codegraphy = forms.ModelChoiceField(queryset=Operation.objects.all())
    operation_need_cloth = forms.BooleanField()
    
    
    
    
    