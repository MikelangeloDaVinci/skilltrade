from urllib import quote_plus

from django.http import HttpResponseRedirect
from django.conf import settings
from re import compile

from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

EXEMPT_URLS = [
    compile(settings.LOGIN_URL.lstrip('/')),
    compile('password/reset\/.*'),
    compile('sign-up\/.*'),
]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(MiddlewareMixin):
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).
    """

    def process_request(self, request):
        # redirect authenticated users at /login/ to index
        if request.get_full_path() == reverse("login"):
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse("index"))

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                print request.get_full_path()
                if request.get_full_path() != "/" and request.get_full_path() != "/logout/":
                    url = settings.LOGIN_URL + "?next=%s" % quote_plus(request.get_full_path())
                else:
                    url = settings.LOGIN_URL
                return HttpResponseRedirect(url)
