from rest_framework import permissions

class IsTeacherOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role.lower() =="teacher"
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.course.tutor.user == request.user