from Radiology.models import Patient, Doctor, MedicalHistory, Insurance
from django.contrib import admin

__author__ = 'Navid'

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',)
    
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('muck',)

class InsuranceAdmin(admin.ModelAdmin):
    list_display=('insurance_type','insurance_category','complementary_insurance')

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(MedicalHistory, MedicalHistoryAdmin)
admin.site.register(Insurance, InsuranceAdmin)
