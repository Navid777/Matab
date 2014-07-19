# -*- coding: utf-8 -*-s
from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import default
from accounting import interface as accounting

# Create your models here.


class MedicalHistory(models.Model):
# todo: complete the fields of this class
    diabet = models.BooleanField(verbose_name=u"دیابت")
    blood_pressure = models.BooleanField(verbose_name=u"فشار خون")
    heart_battery = models.BooleanField(verbose_name=u"باتری قلب")
    artificial_organ = models.BooleanField(verbose_name=u"اندام مصنوعی")
    external_metal = models.BooleanField(verbose_name=u"فلز خارجی")
    metal_clamp = models.BooleanField(verbose_name=u"گیره فلزی")
    protez = models.BooleanField(verbose_name=u"پروتز")
    organ_disability = models.BooleanField(verbose_name=u"عضو ناکارآمد")
    uncontrolable_tension = models.BooleanField(verbose_name=u"تشنج غیرقابل کنترل")
    pregnancy = models.BooleanField(verbose_name=u"بارداری")
    surgery = models.BooleanField(verbose_name=u"جراحی")
    trauma = models.BooleanField(verbose_name=u"زخم")
    malt_fever = models.BooleanField(verbose_name=u"تب مالت")
    anemia = models.BooleanField(verbose_name=u"کم خونی")
    thyroid = models.BooleanField(verbose_name=u"تیرویید")
    #TODO: tarjomeye ina peida beshe!
    history = models.CharField(null=True, blank=True, max_length=300, verbose_name=u"شرح حال")
    comment = models.CharField(null=True, blank=True, max_length=300, verbose_name=u"توضیحات")
    special_disease = models.CharField(null=True, blank=True, max_length=300, verbose_name="بیماری خاص")
    
    def medical_attrs(self):
        for attr, value in self.__dict__.iteritems():
            yield attr, value


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


class Technician(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    national_code = models.IntegerField(max_length=20, unique=True)
    operation = models.CharField(max_length=30)


class Therapist(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    medical_number = models.IntegerField(unique=True)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Appointment(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    national_code = models.CharField(max_length=30, null=True, blank=True)
    day = models.DateField()
    start_time = models.TimeField()
    visited = models.BooleanField(default=False)



class ComplementaryInsurance(models.Model):
    type = models.CharField(max_length=100)
    account_id = models.IntegerField()
    ACCOUNT_SERIES = 4000
    
class Insurance(models.Model):
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    ACCOUNT_SERIES = 3000
    account_id = models.IntegerField()
    portion = models.IntegerField()

    def __unicode__(self):
        return self.type+" "+self.category


class Factor(models.Model):
    #patient information
    patient_first_name = models.CharField(max_length=30)
    patient_last_name = models.CharField(max_length=50)
    patient_national_code = models.IntegerField()
    patient_account_id = models.IntegerField()
    
    #personnel information
    receptor_first_name = models.CharField(max_length=50)
    receptor_last_name = models.CharField(max_length=50)
    operator_first_name = models.CharField(max_length=50, null=True, blank=True)
    operator_last_name = models.CharField(max_length=50, null=True, blank=True)
    technician_first_name = models.CharField(max_length=50, null=True, blank=True)
    technician_last_name = models.CharField(max_length=50, null=True, blank=True)
    therapist_first_name = models.CharField(max_length=30)
    therapist_last_name = models.CharField(max_length=50)
    therapist_medical_number = models.CharField(max_length=20)
    therapist_visit_date = models.DateField(null=True, blank=True)
    
    #operation information
    operation_id = models.IntegerField()
    operation_type = models.CharField(max_length=30)
    operation_name = models.CharField(max_length=30)
    operation_codeography = models.IntegerField()
    operation_cloth = models.BooleanField()
    operation_governmental_fee = models.FloatField()
    operation_individual_fee = models.FloatField()
    operation_medical_fee = models.FloatField()
    operation_film_name = models.CharField(max_length=100, null=True, blank=True)
    operation_film_quantity = models.CharField(max_length=100, null=True, blank=True)
    operation_film_fee = models.FloatField()
    operation_cloth_fee = models.FloatField()
    
    #insurance information
    insurance_type = models.CharField(max_length=100)
    insurance_category = models.CharField(max_length=100)
    insurance_has_complementary = models.BooleanField()
    insurance_complementary = models.CharField(max_length=100, null=True, blank=True)
    insurance_portion = models.IntegerField()
    insurance_serial = models.CharField(max_length=20)
    insurance_page = models.CharField(max_length=20)
    insurance_account_id = models.IntegerField()
    insurance_complementary_account_id = models.IntegerField(null=True, blank=True)
    insurance_exp_date = models.DateField()
    
    #payment information
    patient_payable = models.FloatField()
    discount = models.FloatField(null=True, blank=True)
    patient_share = models.FloatField()
    insurance_share = models.FloatField()
    insurance_complementary_share = models.FloatField()
    patient_paid_amount = models.FloatField(null=True, blank=True)
    insurance_paid = models.BooleanField(default=False)
    complementary_paid = models.BooleanField(default=False)
    comment = models.CharField(null=True, blank=True, max_length=300)
    payment_type = models.IntegerField(null=True, blank=True)
    PAYMENT_TYPES = {
        "CASH": 1,
        "CARD": 2,
    }
    
    #date
    factor_date = models.DateField()
    
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
            codeography=self.operation_codeography,
            name=self.operation_name,
        )

    def get_insurance(self):
        return Insurance.objects.get(
            type=self.insurance_type,
            category=self.insurance_category,
            has_complementary=self.insurance_has_complementary,
            complementary=self.insurance_complementary,
        )
    
    def patient_debt_amount(self):
        return self.patient_payable-self.patient_paid_amount
    
    def patient_paid(self):
        if self.patient_debt_amount():
            return False
        return True
        
    #Adds a discount to factor and returns the remaining amount of discount(if discount is more than factor payable amount
    def add_discount(self, discount):
        if discount == 0:
            return 
        if not self.discount :
            self.discount = 0
        if self.patient_payable < discount:
            self.discount += self.patient_payable
            discount -= self.patient_payable
            self.patient_payable = 0
        else:
            self.discount += discount
            self.patient_payable -= discount
            discount = 0
        self.save()
        return discount
    
    def pay_factor(self, amount):
        if amount == 0 :
            return 
        if amount > self.patient_debt_amount():
            amount -= self.patient_debt_amount()
            accounting.move_credit(self.get_patient().account_id, accounting.get_static_account("office"), 
                               self.patient_debt_amount(), "", "", "", datetime.now(), self.id)
            self.patient_paid_amount += self.patient_debt_amount()
        else:
            self.patient_paid_amount += amount
            accounting.move_credit(self.get_patient().account_id, accounting.get_static_account("office"),
                                amount, "", "", "", datetime.now(), self.id)
            amount = 0
        self.save()
        return amount
    
    def add_comment(self, comment):
        self.comment += "\n" + comment
        self.save()
        
class PatientTurn(models.Model):
    type = models.CharField(max_length=30)
    patient = models.ForeignKey(Patient)
    turn = models.DateTimeField()
    factor = models.ForeignKey(Factor)
    
class Good(models.Model):
    name = models.CharField(max_length=40)
    quantity = models.IntegerField()
    fee = models.FloatField()
    
    CLOTH = u"لباس";
    
    def add_good_to_store(self, quantity):
        factor = GoodFactor()
        factor.good_name = self.name
        factor.good_id = self.id
        factor.good_fee=  self.fee
        factor.quantity = quantity
        factor.date = datetime.now()
        factor.store_quantity_before = self.quantity
        factor.store_quantity_after = self.quantity + quantity
        factor.save()
        self.quantity += quantity
        self.save()
        
    def get_good_from_store(self, quantity):
        factor = GoodFactor()
        factor.good_name = self.name
        factor.good_id = self.id
        factor.good_fee=  self.fee
        factor.quantity = -1 * quantity
        factor.date = datetime.now()
        factor.store_quantity_before = self.quantity
        factor.store_quantity_after = self.quantity - quantity
        factor.save()
        self.quantity -= quantity
        self.save()
    
class Operation(models.Model):
    type = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    codeography = models.IntegerField()
    individual_fee = models.FloatField()
    governmental_fee = models.FloatField()
    medical_fee = models.FloatField()
    film = models.ForeignKey(Good, null=True, blank=True)
    film_quantity = models.IntegerField(null=True, blank=True)

    def __unicode__(self):
        return self.type

#TODO:Systeme anbardari dorost shavad!
class GoodFactor(models.Model): 
    good_id = models.IntegerField()
    good_name = models.CharField(max_length = 30)
    good_fee = models.FloatField()
    quantity = models.IntegerField()
    store_quantity_before = models.IntegerField()
    store_quantity_after = models.IntegerField()
    date = models.DateTimeField()