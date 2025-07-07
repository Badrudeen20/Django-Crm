from functools import wraps 
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse,HttpResponseBadRequest


def permission_required(module):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            auth = authUser(request)
            kwargs['authId'] = auth['id']
            if auth['is_admin']:
                kwargs['roleIds'] = list(Role.objects.all().values_list('id', flat=True))
                kwargs['permission'] = ['View','Add','Edit','Delete']
                kwargs['module'] = list(Module.objects.using('movieplanet').filter(module=module).values_list('module', flat=True))
                kwargs['access'] = True 
                kwargs['isAdmin'] = True
            else:
                kwargs['roleIds'] = list(Roles.objects.using('movieplanet').filter(user_id=auth['id']).values_list('role_id', flat=True))
                permissions = Permission.objects.using('movieplanet').filter(role_id__in=kwargs['roleIds'],modules__module=module).select_related('modules')
                kwargs['permission'] = list(set(
                    p.strip() for perm in permissions.values_list('permission', flat=True) for p in perm.split(',')
                ))
                kwargs['module'] = [permission.modules.module for permission in permissions]
                if module in kwargs['module']:
                    parentIds = list(permissions.filter(~Q(module_parent_id='')).values_list('module_parent_id', flat=True))
                    if parentIds:
                       kwargs['access'] = checkAccess(parentIds,kwargs['roleIds']) 
                    else:
                       kwargs['access'] = True  
                else:
                    kwargs['access'] = False  
                kwargs['isAdmin'] = False
                
            return view(request, *args, **kwargs)     
        return wrapper
    return decorator


def xhr_request_only():
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                auth = authUser(request)
                kwargs['authId'] = auth['id']
                if auth['is_admin']:
                    kwargs['roleIds'] = list(Role.objects.using('movieplanet').all().values_list('id', flat=True))
                    kwargs['module'] = list(Module.objects.using('movieplanet').values_list('module', flat=True))
                    kwargs['isAdmin'] = True
                else:
                    kwargs['roleIds'] = list(Roles.objects.using('movieplanet').filter(user_id=auth['id']).values_list('role_id', flat=True))
                    permissions = Permission.objects.using('movieplanet').filter(role_id__in=kwargs['roleIds'],permission__contains='View').select_related('modules')
                    kwargs['module'] = [permission.modules.module for permission in permissions]
                    kwargs['isAdmin'] = False
                return view(request, *args, **kwargs)  
            else:
                return JsonResponse({
                    "success": False,
                    "error":'Invalid Method!'
                }, status=200)  
        return wrapper
    return decorator


def authUser(req):
    return req.session.get('customer')

def checkAccess(parentId,roleId):
    status = False
    def recurse(mId,rId):
        nonlocal status
        if mId and rId:
            permissions = Permission.objects.using('movieplanet').filter(modules_id__in=mId,role_id__in=rId)
            if permissions.exists():
                mId = list(
                    permissions.filter(
                        Q(~Q(module_parent_id='')) | Q(module_parent_id__in=mId)
                    ).values_list('module_parent_id', flat=True)
                )
                status = True
                recurse(mId,rId)
            else:
               status = False 
    recurse(parentId,roleId)
    return status