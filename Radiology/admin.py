from Radiology.models import Patient, Doctor, MedicalHistory, Insurance, \
    Operation, Therapist, PatientTurn, Factor
from django.contrib import admin

class PatientAdmin(admin.ModelAdmin):
    pass

class DoctorAdmin(admin.ModelAdmin):
    pass
    
class MedicalHistoryAdmin(admin.ModelAdmin):
    pass

class InsuranceAdmin(admin.ModelAdmin):
    pass

class OperationAdmin(admin.ModelAdmin):
    pass

class TherapistAdmin(admin.ModelAdmin):
    pass

class PatientTurnAdmin(admin.ModelAdmin):
    pass

class FactorAdmin(admin.ModelAdmin):
    pass

admin.site.register(Patient, PatientAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(MedicalHistory, MedicalHistoryAdmin)
admin.site.register(Insurance, InsuranceAdmin)
admin.site.register(Operation, OperationAdmin)
admin.site.register(Therapist, TherapistAdmin)
admin.site.register(PatientTurn, PatientTurnAdmin)
admin.site.register(Factor, FactorAdmin)