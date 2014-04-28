from Radiology.models import Patient, Doctor, MedicalHistory, Insurance, \
    Operation, Therapist
from django.contrib import admin

__author__ = 'Navid'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('diabet',)

class InsuranceAdmin(admin.ModelAdmin):
    pass

class OperationAdmin(admin.ModelAdmin):
    list_display=('type', 'codegraphy')

class TherapistAdmin(admin.ModelAdmin):
    list_display=('first_name', 'last_name', 'medical_number')

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(MedicalHistory, MedicalHistoryAdmin)
admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Therapist, TherapistAdmin)

