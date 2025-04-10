import logging
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
logger = logging.getLogger(__name__)

class AuthMiddlewere(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # url = request.path
        url = request.path_info  
        if request.session.get('customer'):
            if request.path == '/movieplanet/login' or request.path == '/movieplanet/signup':
                return redirect('movieplanet:dashboard')
            else:
                return self.get_response(request)
        else:
            # is_admin = request.path.strip("/").split("/")[0]
            if url.startswith('/movieplanet/admin/'):
               return redirect('movieplanet:movieplanet-login')
               # return HttpResponseRedirect(reverse('login'))
            else:
               return self.get_response(request)
