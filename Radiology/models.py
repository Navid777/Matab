# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class MedicalHistory(models.Model):
# todo: complete the fields of this class
    muck = models.BooleanField()


class Patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    national_code = models.IntegerField(unique=True)
    ACCOUNT_SERIES = 1000
    account_id = models.IntegerField()
    medical_history = models.OneToOneField(MedicalHistory, null=True, blank=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    ACCOUNT_SERIES = 2000
    account_id = models.IntegerField()
    medical_number = models.IntegerField(unique=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Therapist(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    medical_number = models.IntegerField(unique=True)
    
    def __unicode__(self):
        return self.first_name + " " + self.last_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Operation(models.Model):
    type = models.CharField(max_length=30)
    codegraphy = models.CharField(max_length=30)
    need_cloth = models.BooleanField()

    def __unicode__(self):
        return self.type


class Visit(models.Model):
    appointment = models.OneToOneField(Appointment)


class Insurance(models.Model):
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    complementary = models.CharField(max_length=100)
    ACCOUNT_SERIES = 3000
    account_id = models.IntegerField()
    portion = models.IntegerField()
    complementary_portion = models.IntegerField()

    def __unicode__(self):
        return self.type+" "+self.category
