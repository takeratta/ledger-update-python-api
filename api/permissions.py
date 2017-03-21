from rest_framework import permissions
from django.db.models import Max

class IsAdminOrReadOnly(permissions.BasePermission): #function that should not be used. Use contrib.auth.has_perm instead
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            access_right = obj.Administration_set.filter(group__in = request.user.groups).aggregate(Max('access_right'))
            return access_right >= 3
        except:
            return False