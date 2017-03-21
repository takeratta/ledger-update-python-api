from rest_framework import permissions
from django.db.models import Max

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.has_perm('api.delete_'+obj.__name__)