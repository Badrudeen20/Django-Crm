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
            if auth['is_admin']:
                kwargs['roleIds'] = list(Role.objects.all().values_list('id', flat=True))
                kwargs['permission'] = ['View','Add','Edit','Delete']
                kwargs['module'] = list(Module.objects.using('default').filter(module=module).values_list('module', flat=True))
                kwargs['access'] = True 
            else:
                kwargs['roleIds'] = list(Roles.objects.using('default').filter(user_id=auth['id']).values_list('role_id', flat=True))
                permissions = Permission.objects.using('default').filter(role_id__in=kwargs['roleIds'],modules__module=module).select_related('modules')
                kwargs['permission'] = list(set(
                    p.strip() for perm in permissions.values_list('permission', flat=True) for p in perm.split(',')
                ))
                kwargs['module'] = [permission.modules.module for permission in permissions]
                parentIds = list(permissions.values_list('module_parent_id', flat=True))
                kwargs['access'] = checkAccess(parentIds,kwargs['roleIds']) 
            return view(request, *args, **kwargs)     
        return wrapper
    return decorator


def xhr_request_only():
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                auth = authUser(request)
                if auth['is_admin']:
                    kwargs['roleIds'] = list(Role.objects.using('default').all().values_list('id', flat=True))
                    kwargs['module'] = list(Module.objects.using('default').values_list('module', flat=True))
                    
                else:
                    # kwargs['permission'] = list(Permission.objects.filter(role_id__in=kwargs['roleIds'],modules__module=module).select_related('modules'))
                    # Many to Many
                    # kwargs['permission'] = list(Permission.objects.filter(role_id__in=kwargs['roleIds'],modules__module=module).prefetch_related('modules'))
                    # kwargs['permission'] = list(Permission.objects.filter(role_id__in=kwargs['roleIds'],modules__module=module).select_related('modules').values_list('permission',flat=True))
                    kwargs['roleIds'] = list(Roles.objects.using('default').filter(user_id=auth['id']).values_list('role_id', flat=True))
                    permissions = Permission.objects.using('default').filter(role_id__in=kwargs['roleIds'],permission__contains='View').select_related('modules')
                    kwargs['module'] = [permission.modules.module for permission in permissions]
                return view(request, *args, **kwargs)  
            else:
                return JsonResponse({
                    "success": False,
                    "error":'Invalid Method!'
                }, status=200)  
        return wrapper
    return decorator


def authUser(req):
    return req.session.get('user')

def checkAccess(parentId,roleId):
    status = False
    def recurse(mId,rId):
        nonlocal status
        if mId and rId:
            permissions = Permission.objects.using('default').filter(modules_id__in=mId,role_id__in=rId)
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