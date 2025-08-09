# utils/decorators.py
from django.shortcuts import redirect
from .models import UserProfile
# def custom_login_required(view_func):
#     def wrapper(request, *args, **kwargs):
#         if request.session.get('userprofile_id'):
#             return view_func(request, *args, **kwargs)
#         else:
#             return redirect('login')
#     return wrapper

def custom_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        username = request.session.get('username')
        if not username:
            return redirect('login')  # or your login page name

        try:
            user = UserProfile.objects.get(username=username)
            request.user = user  # 🟢 Set the actual user object
        except UserProfile.DoesNotExist:
            return redirect('login')

        return view_func(request, *args, **kwargs)
    return wrapper