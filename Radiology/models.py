# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Person(models.Model):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length= 30)
    def __unicode__(self):
        return self.first_name+' '+ self.last_name

class MedicalHistory(models.Model):
# todo: complete the fields of this class
    muck = models.BooleanField()

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    national_code = models.IntegerField(unique=True)
    medical_history = models.OneToOneField(MedicalHistory, null=True, blank=True)

class Doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    medical_number = models.IntegerField(unique=True)

class Operation(models.Model):
    time = models.DateTimeField()

class Appointment(models.Model):
    patient = models.ForeignKey(Patient)
    doctor = models.ForeignKey(Doctor)
    operation = models.ForeignKey(Operation)
    
class Insurance(models.Model):
    name = models.CharField(max_length=100)
    percentage = models.IntegerField()

class MRI(models.Model) :
    operation = models.ForeignKey(Operation)

class Scan(models.Model) :
    operation = models.ForeignKey(Operation)

class Radiology(models.Model) :
    operation = models.ForeignKey(Operation)

class Sonography(models.Model) :
    operation = models.ForeignKey(Operation)

