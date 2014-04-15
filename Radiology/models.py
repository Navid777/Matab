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
    medical_history = models.OneToOneField(MedicalHistory, null=True, blank=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    medical_number = models.IntegerField(unique=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    day = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()


class Visit(models.Model):
    appointment = models.OneToOneField(Appointment)


class Insurance(models.Model):
    insurance_type = models.CharField(max_length=100)
    insurance_category = models.CharField(max_length=100)
    complementary_insurance = models.BooleanField()
    percentage = models.IntegerField()
    def __unicode__(self):
        return self.insurance_type+" "+self.insurance_category


class MRI(models.Model):
    appointment = models.OneToOneField(Appointment)


class Scan(models.Model):
    appointment = models.OneToOneField(Appointment)


class Radiology(models.Model):
    appointment = models.OneToOneField(Appointment)


class Sonography(models.Model):
    appointment = models.OneToOneField(Appointment)
