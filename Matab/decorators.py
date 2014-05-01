from django.http import HttpResponseRedirect

def doctor_in_session(function):
    def wrap(request, *args, **kw):
        if not request.session.get('doctor'):
            return HttpResponseRedirect('/doctor_enroll/')
        else:
            return function(request, *args, **kw)
    return wrap