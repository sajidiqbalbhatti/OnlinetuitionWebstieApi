# urls.py
from django.urls import path
from teacher.views import (
    TeacherListView,
    TeacherProfileManageView,
    TeacherCreateView,
)

app_name = "teacher"

urlpatterns = [
    # ------------------------------------------------------------------
    # Teacher Endpoints
    # ------------------------------------------------------------------
    
    # List all teachers
    path("profile/", TeacherListView.as_view(), name="teacher-list"),
    
    # Create a teacher profile (only for authenticated teachers)
    path("profile/create/", TeacherCreateView.as_view(), name="teacher-create"),
    
    # Retrieve, update, or delete the logged-in teacher's profile
    path("profile/<int:pk>/", TeacherProfileManageView.as_view(), name="teacher-detail"),
]
