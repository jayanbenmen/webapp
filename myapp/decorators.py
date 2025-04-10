from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group

def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.groups.filter(name='student').exists():
                return redirect('studenthome')
            elif request.user.groups.filter(name='teacher').exists():
                return redirect('teacherhome')
            elif request.user.groups.filter(name='admin').exists():
                return redirect('adminhome')
            else:
                return HttpResponse("Unauthorized access. Please contact support.")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page.')
        return wrapper_func
    return decorator