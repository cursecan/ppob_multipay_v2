from django.core.exceptions import PermissionDenied
from userprofile.models import Profile


def user_is_related_agen(function):
    def wrap(request, *args, **kwargs):
        profile_obj = Profile.objects.get(pk=kwargs['id']) # id is profile id

        # Pass for Super Admin
        if request.user.is_superuser:
            return function(request, *args, **kwargs)

        # Related agne only
        if profile_obj.agen == request.user:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def user_is_agen(function):
    def wrap(request, *args, **kwargs):
        # Pass for Super Admin
        if request.user.is_superuser:
            return function(request, *args, **kwargs)

        # Related agne only
        print(request.user.profile.user_type)
        if request.user.profile.user_type == 2:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap