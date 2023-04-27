from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsEmailVerifiedAndAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return (bool(request.user and request.user.is_authenticated) 
                and request.user.email_confirmed)
