from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from movieplanet.models import *
from django.db.models import Q
from django.contrib import messages 
from django.conf import settings
import json
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
import os
import openpyxl
from datetime import datetime
from movieplanet.decorators import (
   permission_required,xhr_request_only
)
######### Admin ##########

@permission_required('Permission')
def permission(request,*args,**kwargs):
    if 'Permission' in kwargs.get('module') and kwargs.get('access'):
      if request.method == 'POST':
            start = request.POST['start']
            length = request.POST['length']
            search = request.POST['search']
            startIndex = (int(start)-1) * int(length)
            endIndex = startIndex + int(length)
            listData = []
            if search :
                  data = Role.objects.filter(name__contains=search,id__in=[1,2])[startIndex:endIndex].all()
                  totalLen = list(Role.objects.filter(name__contains=search,id__in=[1,2]).all())
            else:
                  data = Role.objects.filter(id__in=[1,2])[startIndex:endIndex].all()
                  totalLen = list(Role.objects.filter(id__in=[1,2]).all())
            

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

            # elif action == 'EDIT':
            #    pass
            # else:
            #    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
      else:
            return render(request,"movieplanet/admin/permission.html")
    else:
      return render(request,"movieplanet/404.html")  

def profile(request):
    pass

def dashboard(request):
    # print(request.session.get('customer'))
    return render(request,"movieplanet/admin/dashboard.html")

@permission_required('Menu') 
def menu(request,*args,**kwargs):
    if 'Menu' in kwargs.get('module') and kwargs.get('access'):
      if request.method == 'POST':
            parentId = kwargs.get('parentId', '')
            start = request.POST['start']
            length = request.POST['length']
            search = request.POST['search']
            startIndex = (int(start)-1) * int(length)
            endIndex = startIndex + int(length)
            file_path = os.path.join(settings.BASE_DIR, 'movieplanet', 'menubar.json')
            listData = []
            with open(file_path, 'r') as file:
                  menus =  json.load(file)
                  m = []
                  if parentId:
                     menus = menuFind(menus,parentId)
                  
                  
                  if search :
                        data = menus[int(startIndex):int(endIndex)]
                  else:
                        data = menus[int(startIndex):int(endIndex)]
                        
                  totalLen = 1
                  for idx in menus:
                        if 'parentId' not in idx:
                              totalLen +=1  
                  for m in data: 
                        name = m['name']
                        id = m['id']
                        if parentId:
                              if m['type']=='folder':
                                    name = f'<a href="{settings.BASE_URL}movieplanet/admin/website/menu/{id}">{name}</a>'
                              elif m['type']=='file':
                                    name = f'<a href="#">{name}</a>'
                              post = {
                                    "id":id,
                                    "name":name,
                                    "action":'<button class="btn btn-primary">Update</button>'
                              }      
                              listData.append(post)
                        else:
                              if 'parentId' not in m:
                                    if m['type']=='folder':
                                          name = f'<a href="{settings.BASE_URL}movieplanet/admin/website/menu/{id}">{name}</a>'
                                    elif m['type']=='file':
                                          name = f'<a href="#">{name}</a>'
                                    post = {
                                          "id":id,
                                          "name":name,
                                          "action":'<button class="btn btn-primary">Update</button>'
                                    }      
                                    listData.append(post)

            return JsonResponse({
            "success": True,
            "iTotalRecords":totalLen,
            "iTotalDisplayRecords":totalLen,
            "aaData":listData
            }, status=200)
      else:
            return render(request,"movieplanet/admin/menu.html")
    else:
      return render(request,"movieplanet/404.html")   

def menuFind(menus, pid):
    result = []
    for m in menus:
        if 'parentId' in m and m['parentId'] == pid:
            result.append(m) 
    return result

@permission_required('Posts') 
def posts(request,*args,**kwargs):
    if 'Posts' in kwargs.get('module') and kwargs.get('access'):
      if request.method == 'POST':
            start = request.POST['start']
            length = request.POST['length']
            search = request.POST['search']
            startIndex = (int(start)-1) * int(length)
            endIndex = startIndex + int(length)
            
            
            if search :
                  data = Posts.objects.filter(name__contains=search,status=1)[startIndex:endIndex].all()
                  totalLen = Posts.objects.filter(name__contains=search,status=1).count()
            
            else:
                  data = Posts.objects.filter(status=1).all()[startIndex:endIndex]
                  totalLen = Posts.objects.filter(status=1).count()
            
            listData = []
            for i in data:
                  post = {
                        "id":i.id,
                        "name":i.name,
                        "image":f'<img src={i.image}/>',
                        "rate":i.rate,
                        "action":(f'<button class="btn btn-primary">Edit</button>'
                              f'<button class="btn btn-danger">Delete</button>')

                  }
                        
                  listData.append(post)
            
            return JsonResponse({
                  "success": True,
                  "iTotalRecords":totalLen,
                  "iTotalDisplayRecords":totalLen,
                  "aaData":listData
            }, status=200)
      elif request.method == 'PUT':
            try:
                  body_unicode = request.body.decode('utf-8')
                  if not body_unicode:
                        return JsonResponse({"error": "Empty request body"}, status=400)
                  post = json.loads(body_unicode)
                  Posts.objects.create(
                  name=post['name'],
                  image=post.get('image', ''),
                  rate=post.get('rate', 'N/A'),
                  size=post.get('size', 'N/A'),
                  genre=post.get('genre', 'N/A'),
                  type=post.get('type', 2),
                  lang=post.get('lang', 'N/A'),
                  story=post.get('story', 'N/A'),
                  status=post.get('status', 0),
                  link=post.get('link', '')
                  )

                  return JsonResponse({
                  "status":True,
                  "message":"Inserted success"
                  })
            
            except json.JSONDecodeError:
                  return JsonResponse({"error": "Invalid JSON format"}, status=400)
      else:
            return render(request,"movieplanet/admin/post.html")
    else:
      return render(request,"movieplanet/404.html")  


def excelPost(request,*args,**kwargs):
      try:
            if request.FILES["excel_file"]:
                  excel_file = request.FILES["excel_file"]
                  wb = openpyxl.load_workbook(excel_file)
                  # sheets = wb.sheetnames
                  worksheet = wb["Posts"]
                  # active_sheet = wb.active
                  excel_data = list()
                  for i, row in enumerate(worksheet.iter_rows()):
                        if i == 0:
                           continue 
                        row_data = list()
                        for cell in row:
                              row_data.append(str(cell.value))
                        excel_data.append(row_data)
                  posts = []
                  for row in excel_data:
                        posts.append(Posts(
                              name=row[0],
                              rate=int(row[1]),
                              size=int(row[2]),
                              lang=row[3],
                              image=row[4],
                              genre=row[5],
                              link=row[6],
                              starcast=row[7],
                              type=int(row[8]),
                              status=int(row[9]),
                              # release_date=datetime.strptime(raw_date, "%d-%m-%Y %H:%M:%S"),
                              story=row[11]
                        ))           
                  Posts.objects.bulk_create(posts)
                  return JsonResponse({
                  "status":True,
                  "message":"Inserted success"
                  })
      except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)   

@permission_required('Users')    
def customers(request,*args,**kwargs):
   if 'Users' in kwargs.get('module') and kwargs.get('access'):
      if request.method == 'POST':
            start = request.POST['start']
            length = request.POST['length']
            search = request.POST['search']
            startIndex = (int(start)-1) * int(length)
            endIndex = startIndex + int(length)

            addBtn = ''
            # if 'Add' in kwargs.get('permission'):
            #    addBtn =f'<button class="btn btn-primary" onclick=addEditDelete("Add")>Add User</button>'
            listData = []
            totalLen=0

            if search :
                  data = Customer.objects.filter(is_admin="0",name__contains=search)[startIndex:endIndex].all()
                  totalLen = Customer.objects.filter(is_admin="0",name__contains=search).count()
            else:
                  data = Customer.objects.filter(is_admin="0")[startIndex:endIndex].all()
                  totalLen = Customer.objects.filter(is_admin="0").count()
                  
                  for i in data:
                        # if 'Delete' in kwargs.get('permission'):
                        #       deleteBtn = f'<button class="btn btn-sm  btn-danger" onclick=addEditDelete("Delete",{i.id})>Delete</button>'
                        # else:
                        #       deleteBtn = ''
                        # if 'Edit' in kwargs.get('permission'):
                        #       editBtn = f'<button class="btn btn-sm mx-1 btn-success text-light" onclick=addEditDelete("Edit",{i.id})>Edit</button>'
                        # else:
                        #       editBtn = ''
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
      return render(request,"movieplanet/admin/user.html")
      # return HttpResponseRedirect(request.META['HTTP_REFERER']) 
   else:
      return render(request,"movieplanet/404.html")  


def setting(request):
    pass

    
def module(request,*args,**kwargs):
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
            data = Module.objects.filter(Q(parent_id=parentId),module__contains=search)[startIndex:endIndex].all()
            totalLen = Module.objects.filter(Q(parent_id=parentId),module__contains=search).count()
      else:
            data = Module.objects.filter(Q(parent_id=parentId))[startIndex:endIndex].all()
            totalLen = Module.objects.filter(Q(parent_id=parentId)).count()
      
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
      return render(request,"movieplanet/admin/module.html")
   
@xhr_request_only()
def sidebarList(request,*args,**kwargs):
   
   modules = kwargs.get('module')
   sidebarList =  list(Module.objects.using('movieplanet').filter(module__in=modules).values())
   return JsonResponse({
      "success": True,
      "data":sidebarList
   }, status=200)   

############# Auth ############

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        customer = Customer.authenticate(email=email, password=password)
        if customer:
            request.session['customer'] = json.loads(
                  json.dumps({
                        'id': customer.id,
                        'name': customer.name,
                        'email': customer.email,
                        'is_admin':customer.is_admin
                  }, cls=DjangoJSONEncoder)
            )
            return redirect('admin/dashboard')
            # return HttpResponse(f"Welcome {customer.name}!")
        else:
            return HttpResponseRedirect(reverse('movieplanet:movieplanet-login'))
    else:
      return render(request,"movieplanet/login.html")
   
def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        password = request.POST['password']
        if Customer.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please log in or use another email.")
            return HttpResponseRedirect(reverse('movieplanet-signup'))
        customer = Customer(email=email, name=name,is_admin=0)
        customer.set_password(password)
        customer.save()
        return redirect('admin/dashboard')
        # return HttpResponseRedirect(reverse('admin/dashboard')) 
    else:
      return render(request,"movieplanet/signup.html")

def logout(request):
    request.session.flush()
    return HttpResponse("Logged out successfully!")



########## Frontend ################

def home(request):
    if request.method == 'POST':
      start = request.POST['start']
      length = request.POST['length']
      search = request.POST['search']
      startIndex = (int(start)-1) * int(length)
      endIndex = startIndex + int(length)
      
      
      if search :
            data = Posts.objects.filter(name__contains=search,status=1)[startIndex:endIndex].all()
            totalLen = Posts.objects.filter(name__contains=search,status=1).count()
      
      else:
            data = Posts.objects.filter(status=1).all()[startIndex:endIndex]
            totalLen = Posts.objects.filter(status=1).count()
      
      listData = []
      for i in data:
            post = {
                  "id":i.id,
                  "name":i.name,
                  "image":i.image,
                  "rate":i.rate,
            }
                  
            listData.append(post)
      
      return JsonResponse({
      "success": True,
      "iTotalRecords":totalLen,
      "iTotalDisplayRecords":totalLen,
      "aaData":listData
      }, status=200)
    else:
      return render(request,"movieplanet/home.html")




def postDetailView(request,Link=None):
      linkList = Link.split("+")
      MovieName = " ".join(linkList)
      data = Posts.objects.filter(name=MovieName,status=1).values().first()
      context = {
         "link":Link,
         "post":data
      }
      return render(request,"movieplanet/detail.html",context)

def menubar(request,*args,**kwargs):
      file_path = os.path.join(settings.BASE_DIR, 'movieplanet', 'menubar.json')
      try:
            with open(file_path, 'r') as file:
                  menus =  json.load(file)
                  MenuHtml = ''
                  for m in menus:
                        
                        if 'parentId' not in m:
                              if m['type'] == 'folder':
                                    MenuHtml += (f'<li><button class="nav-link dropdown-btn" data-dropdown="dropdown{m["id"]}" aria-haspopup="true" aria-expanded="false" aria-label="discover">{m["name"]}<i class="bx bx-chevron-down" aria-hidden="true"></i></button>'
                                                f'{menuLoop(menus,m["id"])}'
                                                f'</li>')
                              elif m['type']=='file':  
                                    MenuHtml += (f'<li><a class="nav-link dropdown-link dropdown-btn" data-dropdown="dropdown{m["id"]}" href="#" aria-haspopup="true" aria-expanded="false">{m["name"]}</a></li>')

                              
                  
            return JsonResponse({"status":True,"Menus":MenuHtml})
      except Exception as e:
            return JsonResponse({"status":False,"error": str(e)}, status=500)


def menuLoop(Menus=[],MenuId=None,IsLoop=None):
   check = False
   menu = f'<div id="dropdown{MenuId}" class="dropdown"><ul role="menu">'
   arrow = ''
   if IsLoop:
      menu = f'<div id="dropdown{MenuId}" class="dropdown loopMenu"><ul role="menu">'
      arrow = '<i class="bx bx-chevron-down" aria-hidden="true"></i>'
   for m in Menus:
      check = True
      
      if 'parentId' in m and m['parentId'] == MenuId:
            if m['type'] == 'folder':
                  menu += (f'<li><button class="nav-link dropdown-btn" data-dropdown="dropdown{m["id"]}" aria-haspopup="true" aria-expanded="false" aria-label="discover">{m["name"]}<i class="bx bx-chevron-down" aria-hidden="true"></i></button>'
                              f'{menuLoop(Menus,m["id"],True)}'
                              f'</li>')
            elif m['type']=='file':  
                 menu += (f'<li><a class="nav-link dropdown-link dropdown-btn" data-dropdown="dropdown{m["id"]}" href="#" aria-haspopup="true" aria-expanded="false">{m["name"]}</a></li>')

                                   
   menu +='</ul></div>'
   if check:
      return menu
   else:    
      return ''

"""

def menu(request,*args,**kwargs):
    parentId = kwargs.get('parentId', '')
    if request.method == 'POST':
      start = request.POST['start']
      length = request.POST['length']
      search = request.POST['search']
      startIndex = (int(start)-1) * int(length)
      endIndex = startIndex + int(length)
      file_path = os.path.join(settings.BASE_DIR, 'movieplanet', 'sidebar.json')
      listData = []
      with open(file_path, 'r') as file:
            menus =  json.load(file)
            m = []
            if parentId:
               menus = menuFind(menus,parentId)
            print(m)
            if search :
                  data = menus[int(startIndex):int(endIndex)]
                  totalLen = len(menus[int(startIndex):int(endIndex)])
            else:
                  
                  data = menus[int(startIndex):int(endIndex)]
                  totalLen = len(menus[int(startIndex):int(endIndex)])
      
            # print(d)
            for i in data:
                  name = i['name']
                  id = i['id']
                  if i['type']=='folder':
                     name = f'<a href="{settings.BASE_URL}movieplanet/admin/website/menu/{id}">{name}</a>'

                  post = {
                        "id":id,
                        "name":name,
                        "action":'<button class="btn btn-primary">Update</button>'
                  }      
                  listData.append(post)
      
      return JsonResponse({
      "success": True,
      "iTotalRecords":totalLen,
      "iTotalDisplayRecords":totalLen,
      "aaData":listData
      }, status=200)
    else:
      return render(request,"movieplanet/admin/menu.html")

def menuFind(menus, idx):
    result = []

    def recurse(items, id):
        nonlocal result  # to modify outer variable
        for item in items:
            if item.get('id') == id and item.get('type') == 'folder':
                result = item.get('children', [])
                return True  # found, stop searching
            if 'children' in item and isinstance(item['children'], list):
                if recurse(item['children'], id):
                    return True  # bubble up success
        return False  # not found in this branch

    recurse(menus, idx)
    return result

def sidebarList(request,*args,**kwargs):
      file_path = os.path.join(settings.BASE_DIR, 'movieplanet', 'sidebar.json')
      try:
            with open(file_path, 'r') as file:
                  menus =  json.load(file)
                  MenuHtml = ''
                  for m in menus:
                        
                        if m['type'] == 'folder':
                              MenuHtml += (f'<li><button class="nav-link dropdown-btn" data-dropdown="dropdown{m["id"]}" aria-haspopup="true" aria-expanded="false" aria-label="discover">{m["name"]}<i class="bx bx-chevron-down" aria-hidden="true"></i></button>'
                                          f'{menuLoop(m["children"],m["id"])}'
                                          f'</li>')
                        elif m['type'] == 'file':
                              MenuHtml += (f'<li><a class="nav-link dropdown-link dropdown-btn" data-dropdown="dropdown{m["id"]}" href="#" aria-haspopup="true" aria-expanded="false">{m["name"]}</a></li>')
                  
            return JsonResponse({"status":True,"Menus":MenuHtml})
      except Exception as e:
            return JsonResponse({"status":False,"error": str(e)}, status=500)


def menuLoop(Menus=[],MenuId=None,IsLoop=None):
   check = False
   if IsLoop:
      menu = f'<div id="dropdown{MenuId}" class="dropdown loopMenu"><ul role="menu">'
      arrow = '<i class="bx bx-chevron-down" aria-hidden="true"></i>'
   else:
      menu = f'<div id="dropdown{MenuId}" class="dropdown"><ul role="menu">'
      arrow = ''
   for m in Menus:
      check = True
      if m['type']=='folder':
            menu += (f'<li><a class="nav-link dropdown-link dropdown-btn" data-dropdown="dropdown{m["id"]}" href="#" aria-haspopup="true" aria-expanded="false">{m["name"]}{arrow}</a>{menuLoop(m["children"],m["id"],True)}</li>')
      elif m['type'] == 'file':
            
            menu += (f'<li><a class="nav-link dropdown-link dropdown-btn" data-dropdown="dropdown{m["id"]}" href="#" aria-haspopup="true" aria-expanded="false">{m["name"]}</a></li>')
               
   menu +='</ul></div>'
   if check:
      return menu
   else:    
      return ''
   

def menuLoop(Menus=[],MenuId=None,IsLoop=None):
   check = False
   if IsLoop:
      menu = f'<div id="dropdown{MenuId}" class="dropdown loopMenu"><ul role="menu">'
      arrow = '<i class="bx bx-chevron-down" aria-hidden="true"></i>'
   else:
      menu = f'<div id="dropdown{MenuId}" class="dropdown"><ul role="menu">'
      arrow = ''
   for m in Menus:
      if m.menuId:
         if m.menuId==str(MenuId):
            check = True
            menu += (f'<li><a class="dropdown-link dropdown-btn" data-dropdown="dropdown{m.id}" href="#" aria-haspopup="true" aria-expanded="false">{m.name}{arrow}</a>{menuLoop(Menus,m.id,True)}</li>')
   menu +='</ul></div>'
   if check:
      return menu
   else:    
      return ''

def menuList(request):
   if request.method == 'POST':
      menus =  Menu.objects.filter(status="1").all()
      MenuHtml = ''
      for m in menus:
         if m.menuId == None:
            MenuHtml += (f'<li><button class="nav-link dropdown-btn" data-dropdown="dropdown{m.id}" aria-haspopup="true" aria-expanded="false" aria-label="discover">{m.name}<i class="bx bx-chevron-down" aria-hidden="true"></i></button>'
                         f'{menuLoop(menus,m.id)}'
                         f'</li>')
      return JsonResponse({
               "Success": True,
               "Menus":MenuHtml
            }, status=200)

def menu(request):

    if request.method == 'POST':
      start = request.POST['start']
      length = request.POST['length']
      search = request.POST['search']
      startIndex = (int(start)-1) * int(length)
      endIndex = startIndex + int(length)
      
      
      if search :
            data = Menu.objects.filter(name__contains=search,status=1)[startIndex:endIndex].all()
            totalLen = Menu.objects.filter(name__contains=search,status=1).count()
      
      else:
            data = Menu.objects.filter(status=1).all()[startIndex:endIndex]
            totalLen = Menu.objects.filter(status=1).count()
      
      listData = []
      for i in data:
            post = {
                  "id":i.id,
                  "name":i.name,
                  "status":i.status
            }
                  
            listData.append(post)
      
      return JsonResponse({
      "success": True,
      "iTotalRecords":totalLen,
      "iTotalDisplayRecords":totalLen,
      "aaData":listData
      }, status=200)
    else:
        return render(request,"movieplanet/admin/menu.html") 
"""