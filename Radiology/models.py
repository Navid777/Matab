# -*- coding: utf-8 -*-s
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default

# Create your models here.


class MedicalHistory(models.Model):
# todo: complete the fields of this class
    diabet = models.BooleanField()
    blood_pressure = models.BooleanField()
    heart_battery = models.BooleanField()
    artificial_organ = models.BooleanField()
    external_metal = models.BooleanField()
    metal_clamp = models.BooleanField()
    protez = models.BooleanField()
    organ_disability = models.BooleanField()
    uncontrolable_tension = models.BooleanField()
    pregnancy = models.BooleanField()
    surgery = models.BooleanField()
    trauma = models.BooleanField()
    malt_fever = models.BooleanField()
    anemia = models.BooleanField()
    thyroid = models.BooleanField()
    #TODO: tarjomeye ina peida beshe!
    history = models.CharField(null=True, blank=True,max_length=300)
    comment = models.CharField(null=True, blank=True,max_length = 300)
    special_disease = models.CharField(null=True, blank=True,max_length = 300)


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    national_code = models.IntegerField(max_length=20, unique=True)
    ACCOUNT_SERIES = 1000
    account_id = models.IntegerField()
    medical_history = models.OneToOneField(MedicalHistory, null=True, blank=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __unicode__(self):
        return self.get_full_name()


class UserType(models.Model):
    MRI_OPERATION = u'MRI'
    TYPES = {
        "RECEPTOR": u'پذیرنده',
        "OPERATOR": u'اپراتور',
    }

    user = models.OneToOneField(User)
    type = models.CharField(max_length=30)
    operation = models.CharField(max_length=30, blank=True, null=True)


class PatientTurn(models.Model):
    type = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient)
    turn = models.DateTimeField()


class Therapist(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    medical_number = models.IntegerField(unique=True)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()



class Visit(models.Model):
    appointment = models.OneToOneField(Appointment)

class ComplementaryInsurance(models.Model):
    type = models.CharField(max_length=100)
    account_id = models.IntegerField(null=True, blank=True)
    def __unicode__(self):
        return self.type

class Insurance(models.Model):
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    ACCOUNT_SERIES = 3000
    account_id = models.IntegerField()
    portion = models.IntegerField()
    has_complementary = models.BooleanField()
    complementary = models.ForeignKey(ComplementaryInsurance)

    def __unicode__(self):
        return self.type+" "+self.category


class Factor(models.Model):
    patient_first_name = models.CharField(max_length=30)
    patient_last_name = models.CharField(max_length=50)
    patient_national_code = models.IntegerField()
    patient_account_id = models.IntegerField()
    receptor_first_name = models.CharField(max_length=50)
    receptor_last_name = models.CharField(max_length=50)
    MRI_operator_first_name = models.CharField(max_length=50, null=True, blank=True)
    MRI_operator_last_name = models.CharField(max_length=50, null=True, blank=True)
    MRI_prepare_first_name = models.CharField(max_length=50, null=True, blank=True)
    therapist_first_name = models.CharField(max_length=30)
    therapist_last_name = models.CharField(max_length=50)
    therapist_medical_number = models.CharField(max_length=20)
    operation_type = models.CharField(max_length=30)
    operation_codeography = models.CharField(max_length=30)
    operation_cloth = models.BooleanField()
    operation_fee = models.FloatField()
    insurance_type = models.CharField(max_length=100)
    insurance_category = models.CharField(max_length=100)
    insurance_has_complementary = models.BooleanField()
    insurance_complementary = models.CharField(max_length=100, null=True, blank=True)
    insurance_portion = models.IntegerField()
    insurance_serial = models.CharField(max_length=20)
    insurance_page = models.CharField(max_length=20)
    insurance_account_id = models.IntegerField()
    insurance_complementary_account_id = models.IntegerField(null=True, blank=True)
    total_fee = models.FloatField()
    patient_share = models.FloatField()
    insurance_share = models.FloatField()
    insurance_complementary_share = models.FloatField()
    patient_paid = models.BooleanField(default=False)
    insurance_paid = models.BooleanField(default=False)
    complementary_paid = models.BooleanField(default=False)

    def get_patient(self):
        return Patient.objects.get(
            first_name=self.patient_first_name,
            last_name=self.patient_last_name,
            national_code=self.patient_national_code,
        )

    def get_therapist(self):
        return Therapist.objects.get(
            first_name=self.therapist_first_name,
            last_name=self.therapist_last_name,
            medical_number=self.therapist_medical_number,
        )

    def get_operation(self):
        return Operation.objects.get(
            type=self.operation_type,
            codeography=self.operation_codeography
        )

    def get_insurance(self):
        return Insurance.objects.get(
            type=self.insurance_type,
            category=self.insurance_category,
            has_complementary=self.insurance_has_complementary,
            complementary=self.insurance_complementary,
        )


class Good(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField()
    fee = models.FloatField()
    
class Operation(models.Model):
    type = models.CharField(max_length=30)
    codeography = models.CharField(max_length=30)
    individual_fee = models.FloatField()
    governmental_fee = models.FloatField()
    medical_fee = models.FloatField()
    film = models.ForeignKey(Good)
    film_quantity = models.IntegerField()

    def __unicode__(self):
        return self.type
