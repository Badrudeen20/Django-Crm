import logging
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
logger = logging.getLogger(__name__)

class DashboardMiddlewere(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        url = request.path
        if request.session.get('user'):
            if request.path == '/admin/login/' or request.path == '/admin/register/':
                return redirect('backend:dashboard')
            else:
                return self.get_response(request)
        else:
            if url =='/admin/login/' or url =='/admin/register/':
               return self.get_response(request)
               # return HttpResponseRedirect(reverse('login'))
            else:
                return redirect('backend:backend-login')
