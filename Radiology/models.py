from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Person(models.Model):
    user = models.ForeignKey(User)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length= 30)
    def __unicode__(self):
        return self.first_name+' '+ self.last_name

class medical_history(models.Model):
# todo: complete the fields of this class
    muck = models.BooleanField()

class patient(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    medical_history = models.OneToOneField(medical_history)

class doctor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    medical_number = models.IntegerField()

class operation(models.Model):
    time = models.DateTimeField()

class appointment(models.Model):
    patient = models.ForeignKey(patient)
    doctor = models.ForeignKey(doctor)
    operation = models.ForeignKey(operation)

class MRI(models.Model) :
    operation = models.ForeignKey(operation)

class scan(models.Model) :
    operation = models.ForeignKey(operation)

class radiology(models.Model) :
    operation = models.ForeignKey(operation)

class sonography(models.Model) :
    operation = models.ForeignKey(operation)

