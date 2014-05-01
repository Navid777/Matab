from django.http import HttpResponseRedirect
from Radiology import views


def exists_in_session(key):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            if key in request.session:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(views.doctor_enroll)
        return wrap
    return decorator