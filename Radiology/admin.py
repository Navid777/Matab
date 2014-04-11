from Radiology.models import Patient, Doctor, MedicalHistory
from django.contrib import admin

__author__ = 'Navid'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('muck',)

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(MedicalHistory, MedicalHistoryAdmin)
