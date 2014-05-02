from django.core.urlresolvers import reverse
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
            return HttpResponseRedirect(reverse('Radiology.views.login_view'))
        else:
            return function(request, *args, **kwargs)
    return wrap


def user_type_comforms_or_404(assertion):
    def decorator(function):
        def wrap(request, *args, **kwargs):
            if assertion(request.user.user_role.type):
                return function(request, *args, **kwargs)
            else:
                raise Http404()
        return wrap
    return decorator