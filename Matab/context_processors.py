from Radiology.models import Patient, Doctor


def fetch_patient(request):
    if 'patient_id' in request.session:
        return {
            'patient': Patient.objects.get(id=request.session['patient_id'])
        }
    return {
        'patient': None
    }


def fetch_doctor(request):
    if 'doctor_id' in request.session:
        return {
            'doctor': Doctor.objects.get(id=request.session['doctor_id'])
        }
    return {
        'doctor': None
    }