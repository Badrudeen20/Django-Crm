from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login,logout
from django import forms
from django.db.models import Q
from django.conf import settings
from .models import *
from django.contrib import messages 
import json
from django.core.serializers.json import DjangoJSONEncoder
from backend.decorators import (
   permission_required,xhr_request_only
)
############# Auth ############

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = User.authenticate(email=email, password=password)
        if user:
            request.session['user'] = json.loads(
                  json.dumps({
                        'id': user.id,
                        'name': user.name,
                        'email': user.email,
                        'is_admin':user.is_admin
                  }, cls=DjangoJSONEncoder)
            )
            return redirect(reverse('backend:dashboard'))
           
        else:
            return HttpResponseRedirect(reverse('backend:backend-login'))
    else:
      return render(request,"backend/login.html")
   
def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please log in or use another email.")
            return HttpResponseRedirect(reverse('backend:backend-register'))
        customer = User(email=email, name=name,is_admin=0)
        customer.set_password(password)
        customer.save()
        return redirect('backend:dashboard')
        # return HttpResponseRedirect(reverse('admin/dashboard')) 
    else:
      return render(request,"backend/register.html")

def logout(request):
    request.session.flush()
    return HttpResponseRedirect(reverse('backend:backend-login'))
    # return HttpResponse("Logged out successfully!")



############ Backend ###############
def dashboard(request,*args,**kwargs):
    return render(request,"backend/admin/dashboard.html")

@xhr_request_only()
def sidebarList(request,*args,**kwargs):
   modules = kwargs.get('module')
   sidebarList =  list(Module.objects.using('default').filter(module__in=modules).values())
   return JsonResponse({
      "success": True,
      "data":sidebarList
   }, status=200)   

@permission_required('Permission')
def permission(request,*args,**kwargs):
   if 'Permission' in kwargs.get('module') and kwargs.get('access'):
      role = kwargs.get('role', '')
      if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'View' in kwargs.get('permission'):
            start = request.POST['start']
            length = request.POST['length']
            search = request.POST['search']
            startIndex = (int(start)-1) * int(length)
            endIndex = startIndex + int(length)
            listData = []
            roles = kwargs.get('roleIds')
            if search :
                  data = Role.objects.using('default').filter(name__contains=search,id__in=roles)[startIndex:endIndex].all()
                  totalLen = list(Role.objects.using('default').filter(name__contains=search,id__in=roles).all())
            else:
                  data = Role.objects.using('default').filter(id__in=roles)[startIndex:endIndex].all()
                  totalLen = list(Role.objects.using('default').filter(id__in=roles).all())

            for i in data:
                  permission = {
                  "id":i.id,
                  "roleName":i.name,
                  "action":(f'<a class="btn btn-primary" href="{settings.BASE_URL}admin/administration/permission/{i.id}" >Permission</a>')
                  }
                  listData.append(permission)

            return JsonResponse({
                  "success": True,
                  "iTotalRecords":len(totalLen),
                  "iTotalDisplayRecords":len(totalLen),
                  "aaData":listData
            }, status=200)
      elif role:
          if 'Edit' in kwargs.get('permission'):
             module = Module.objects.using('default').all()
             if request.method == 'POST':
                
                for m in module:
                    perm = Permission.objects.using('default').filter(modules_id=m.id,role_id=role).first()
                    if m.parent_id=='':
                        if perm:
                              if m.module in request.POST:
                                perm.permission =  request.POST[m.module]
                                perm.save()
                              else:
                                perm.delete()
                        else:
                              if m.module in request.POST:
                                 Permission.objects.using('default').create(
                                    permission=request.POST[m.module],
                                    role_id = role,
                                    modules_id = m.id
                                 )
                    else:
                        if m.parent_id:
                              permission = ''
                              if m.module+'[view]' in request.POST:
                                    permission += request.POST[m.module+'[view]']
                              if m.module+'[add]' in request.POST:
                                    permission +=','+request.POST[m.module+'[add]']
                              if m.module+'[edit]' in request.POST:
                                    permission +=','+request.POST[m.module+'[edit]']
                              if m.module+'[delete]' in request.POST:
                                    permission +=','+request.POST[m.module+'[delete]']
                                       
                              if perm:
                                    if permission:
                                       perm.permission =  permission
                                       perm.save()
                                    else:
                                       perm.delete()  
                              else:
                                  if permission:
                                     Permission.objects.using('default').create(
                                          permission=permission,
                                          role_id = role,
                                          modules_id = m.id,
                                          module_parent_id=m.parent_id
                                     )
                                   
             allow = '<ul class="list-group">'
             for m in module:
                 perm = Permission.objects.using('default').filter(modules_id=m.id,role_id=role).first()
                 if m.parent_id=='':
                       allow +=(f'<li class="list-group-item ">'
                                f'<div class="w-100 d-flex justify-content-between">'
                                f'<div>{m.module}</div>'
                                f'<div>View <input type="checkbox" name="{m.module}" value="View" {"checked" if perm else None} class="form-check-input" /> </div>'
                                f'</div>'
                                f'{checkParent(role,module,m.id)}'
                                f'</li>')   
                    
             allow +='</ul>'
             
             return render(request,"backend/admin/allowpermission.html",{'permissions':allow})
          else:
            return redirect(reverse('backend:backend-permission'))
      else:
            return render(request,"backend/admin/permission.html")
   else:
      return render(request,"backend/404.html")  

def checkParent(role,module,mid):
      allow = '<ul class="list-group">'
      for m in module:
            perm = Permission.objects.using('default').filter(modules_id=m.id,role_id=role).first()
            if m.parent_id == str(mid):
                        checked = []
                        if perm:
                           checked = perm.permission.split(',')
                       
                        allow +=(f'<li class="list-group-item">'
                                    f'<div class="w-100 d-flex justify-content-between">'
                                    f'<div>{m.module}</div>'
                                    f'<div>View <input name="{m.module}[view]" type="checkbox" value="View" {"checked" if "View" in checked else None } class="form-check-input" />'
                                    f'Add <input name="{m.module}[add]" type="checkbox" value="Add" {"checked" if "Add" in checked else None }  class="form-check-input" />' 
                                    f'Edit <input name="{m.module}[edit]" type="checkbox" value="Edit" {"checked" if "Edit" in checked else None } class="form-check-input" />'
                                    f'Delete <input name="{m.module}[delete]" type="checkbox" value="Delete" {"checked" if "Delete" in checked else None } class="form-check-input" /></div>'
                                    f'</div>'
                                    f'{checkParent(role,module,m.id)}'
                                 f'</li>')   
                 
      allow +='</ul>'
      
      return allow




@permission_required('Module')  
def module(request,*args,**kwargs):
   if 'Module' in kwargs.get('module') and kwargs.get('access'):
      parentId = kwargs.get('parentId', '')
      if request.method == 'POST':
            start = request.POST['start']
            length = request.POST['length']
            search = request.POST['search']
            startIndex = (int(start)-1) * int(length)
            endIndex = startIndex + int(length)
            
            listData = []
            totalLen=0
      
            if search :
                  data = Module.objects.using('default').filter(Q(parent_id=parentId),module__contains=search)[startIndex:endIndex].all()
                  totalLen = Module.objects.using('default').filter(Q(parent_id=parentId),module__contains=search).count()
            else:
                  data = Module.objects.using('default').filter(Q(parent_id=parentId))[startIndex:endIndex].all()
                  totalLen = Module.objects.using('default').filter(Q(parent_id=parentId)).count()
            
            for i in data:
                  if i.moduleType=='2':
                        module = f'<a href="{settings.BASE_URL}movieplanet/admin/administration/module/{i.id}">{i.module}</a>'
                  else:
                        module = i.module
                  permission = {
                        "id":i.id,
                        "module":module,
                        "action":(f'<a href="{settings.BASE_URL}movieplanet/admin/administration/module/{i.id}/delete" class="btn btn-sm btn-danger" >Delete</a>')
                  }  
                  listData.append(permission)
            
            return JsonResponse({
            "success": True,
            "iTotalRecords":totalLen,
            "iTotalDisplayRecords":totalLen,
            "aaData":listData
            }, status=200)  
      else:
            return render(request,"backend/admin/module.html")
   else:
      return render(request,"backend/404.html")    



@permission_required('Users')  
def users(request,*args,**kwargs):
    if 'Users' in kwargs.get('module') and kwargs.get('access'):
      if request.method == 'POST':
            start = request.POST['start']
            length = request.POST['length']
            search = request.POST['search']
            startIndex = (int(start)-1) * int(length)
            endIndex = startIndex + int(length)

            addBtn = ''
            listData = []
            totalLen=0

            if search :
                  data = User.objects.using('default').filter(is_admin="0",name__contains=search)[startIndex:endIndex].all()
                  totalLen = User.objects.using('default').filter(is_admin="0",name__contains=search).count()
            else:
                  data = User.objects.using('default').filter(is_admin="0")[startIndex:endIndex].all()
                  totalLen = User.objects.using('default').filter(is_admin="0").count()
                  
                  for i in data:
                        deleteBtn = ''
                        editBtn=''
                        obj = {
                              "id":i.id,
                              "name":i.name,
                              "email":i.email,
                              "action":(
                                    f'<button  onclick=userRole({i.id}) class="btn btn-sm btn-info mx-1 text-light">Role</button>'
                                    f'{editBtn}'
                                    f'{deleteBtn}'  
                                    )
                        }  
                        
                        listData.append(obj)

            return JsonResponse({
                        "success": True,
                        "iTotalRecords":totalLen,
                        "iTotalDisplayRecords":totalLen,
                        "aaData":listData,
                        "permission":addBtn
                  }, status=200)
      return render(request,"backend/admin/user.html")
      # return HttpResponseRedirect(request.META['HTTP_REFERER']) 
    else:
      return render(request,"backend/404.html")       





"""
def notfound(request):
    return render(request,"backend/404.html")  

def redirect(request):
    return render(request,"index.html")

allow = {}
for m in module:
      allow[m.module]= {}
      perm = Permission.objects.using('default').filter(modules_id=m.id,role_id=role).first()
      allow[m.module]['name'] = perm.permission if perm else None
      allow[m.module]['module_id'] = perm.modules_id if perm else None
      allow[m.module]['module_parent_id'] = perm.module_parent_id if perm else None

def adminLogin(request):
   if request.method == 'POST':
         username = request.POST['username']
         password = request.POST['password']
         user = authenticate(request, username=username, password=password)
         if user is not None:
               login(request, user)
               return HttpResponseRedirect(reverse('dashboard')) 
         
   return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
            username = request.POST['username']
            email =  request.POST['email']
            password =  request.POST['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username = username, password = password)
                login(request, user)
                return redirect('login')   
            

    return render(request, 'register.html')

def adminLogout(request):
    if request.user.is_authenticated:
      logout(request)  
    return HttpResponseRedirect(reverse('login')) 

"""

  
