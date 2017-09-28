from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import translation

class No404Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        if response.status_code == 404:
            messages.success(request, 'Elemento no encontrado')
            return HttpResponseRedirect(reverse('news_list'))
        return response


from django.conf import settings
from django.utils import translation


class LocaleMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        try:
            cookie = settings.LANGUAGE_COOKIE_NAME
        except AttributeError:
            cookie = 'language'
        forced_lang = request.GET.get(cookie, None)
        request.forced_lang = forced_lang
        if forced_lang:
            translation.activate(forced_lang)
            request.LANGUAGE_CODE = translation.get_language()
            if hasattr(request, 'session'):
                request.session[translation.LANGUAGE_SESSION_KEY] = forced_lang

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response