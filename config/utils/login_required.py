from functools import wraps
from django.contrib.auth.decorators import user_passes_test

def login_check(function=None, arg1=None, arg2=None):
    def check_login(user):
        return user.is_authenticated

    def decorator(view_func):
        decorated_view_func = user_passes_test(check_login)(view_func)
        return decorated_view_func

    if function is None:
        return decorator
    else:
        return decorator(function)