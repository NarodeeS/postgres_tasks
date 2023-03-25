from rest_framework import permissions

from .models import DatabaseInfo, UserTask


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        request_user = request.user
        
        if isinstance(obj, DatabaseInfo):
            print('here')
            return obj.user_task.user == request_user
        elif isinstance(obj, UserTask):
            print('here')
            return obj.user == request_user
        else:
            return False
