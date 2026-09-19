"""
Session-based authentication layer for MealBox.

Replaces django.contrib.auth entirely.

Session key: 'user_id' -> User.pk
"""

from functools import wraps
from django.shortcuts import redirect
from .models import User


SESSION_KEY = 'user_id'


# ----------------------------------------------------------------------
# Session helpers
# ----------------------------------------------------------------------
def login_user(request, user):
    """Persist the user's id in the session."""
    request.session[SESSION_KEY] = user.pk


def logout_user(request):
    """Clear the user's session."""
    request.session.pop(SESSION_KEY, None)


def get_current_user(request):
    """Return the logged-in User instance, or None."""
    user_id = request.session.get(SESSION_KEY)
    if not user_id:
        return None
    return User.objects.filter(pk=user_id, is_active=True).first()


# ----------------------------------------------------------------------
# Decorator
# ----------------------------------------------------------------------
def login_required(view_func):
    """Redirect anonymous users to the login page."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get(SESSION_KEY):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
