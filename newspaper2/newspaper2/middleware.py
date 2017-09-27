from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

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