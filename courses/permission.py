from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

class IsCourseTutor(permissions.BasePermission):
    """
    Only the tutor who owns the course can update or delete it.
    """
    def has_permission(self, request, view):
        # Allow GET for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # User should be authenticated
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated(detail="Please login first...")
        
        return True

    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS sab allow hain
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only the course tutor can update/delete
        if hasattr(request.user, "teacher_profile"):
            return obj.tutor == request.user.teacher_profile
        
        raise PermissionDenied(detail="You are not the tutor of this course.")
