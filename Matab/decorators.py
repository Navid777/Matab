from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect
from django.http.response import Http404


def exists_in_session_or_redirect(key, url):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            if key in request.session:
                return function(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(url)

        return wrap

    return decorator


def user_logged_in(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_anonymous():
            return HttpResponseRedirect(reverse_lazy('Radiology.views.login_view'))
        else:
            return function(request, *args, **kwargs)

    return wrap


def user_is_staff_or_404(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_staff:
            return function(request, *args, **kwargs)
        else:
            raise Http404()

    return wrap


def user_type_conforms_or_404(assertion):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            if assertion(request.user.usertype.type):
                return function(request, *args, **kwargs)
            else:
                raise Http404()

        return wrap

    return decorator