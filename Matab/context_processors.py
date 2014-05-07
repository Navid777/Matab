from Radiology.models import Patient, UserType


def fetch_static_types(request):
    return {
        'MRI_OPERATION': UserType.MRI_OPERATION,
        'USER_TYPES': UserType.TYPES,
    }


def fetch_patient(request):
    if 'patient_id' in request.session:
        return {
            'patient': Patient.objects.get(id=request.session['patient_id'])
        }
    return {
        'patient': None
    }