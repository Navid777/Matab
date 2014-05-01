from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


def exists_in_session(key):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            if key in request.session:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('Radiology.views.doctor_enroll'))
        return wrap
    return decorator