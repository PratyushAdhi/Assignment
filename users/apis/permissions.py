from rest_framework import permissions

class IsTeacherOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_teacher or obj.is_admin:
            return True
        return False

class IsOwnerOrTeacherOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_teacher or obj.is_admin:
            return True
        elif obj.email == request.user.email:
            return True
        return False

class IsAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_admin:
            return True
        return False

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.is_admin:
            return True
        elif obj.email == request.user.email:
            return True
        return False
