from Radiology.models import Patient, UserType, Technician, Good


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


def fetch_technician(request):
    if 'technician_id' in request.session:
        return {
            'technician': Technician.objects.get(id=request.session['technician_id'])
        }
    return {
        'technician': None
    }

def fetch_limited_goods(request):
    return {
            'limited_goods': Good.objects.filter(quantity__lte=30)
    }