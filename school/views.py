from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

class Activity(View):
    def get(self, request, *args, **kwargs):
        action = kwargs.get('action')
        if action == 'detail':
            return self.detail(request)
        return HttpResponse('GET response')

    def post(self, request, *args, **kwargs):
        return HttpResponse('POST response')

    def put(self, request, *args, **kwargs):
        return HttpResponse('PUT response')
    
    def patch(self, request, *args, **kwargs):
        return HttpResponse('PATCH response')
    
    def detail(self, request):
        return HttpResponse('detail')

class Notice(View):
    def get(self, request):
        return HttpResponse('result')
    
class Home(View):
    def get(self, request):
        return render(request, 'school/home.html')