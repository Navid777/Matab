from Radiology.models import Patient, UserType


def fetch_static_types(request):
    return {
        'MRI_TYPE': UserType.MRI,
        'RECEPTOR_TYPE': UserType.RECEPTOR,
    }


def fetch_patient(request):
    if 'patient_id' in request.session:
        return {
            'patient': Patient.objects.get(id=request.session['patient_id'])
        }
    return {
        'patient': None
    }