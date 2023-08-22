from django.http import HttpResponse
from django.shortcuts import redirect

# if request.user.is_authenticated:
#         return redirect('/')

def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper

def allowed_access(allowed_groups=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_groups:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("<h1>403 Forbidden</h1>")
        return wrapper
    return decorator

def admin_only(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

            if group == 'customer':
                return redirect("/user")
            if group == "admin" or group == 'employee':
                return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("<h1>403 Forbidden</h1>")
    return wrapper