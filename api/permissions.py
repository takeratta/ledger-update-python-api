from rest_framework import permissions
from django.db.models import Max

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        try:
            access_rights = obj.access.filter(user = request.user).aggregate(Max('role'))
            if access_rights[0].role >= 3 :  #3 is a placeholder for defining level of admin/role for this object
                return True
        except:
            return False
        return False