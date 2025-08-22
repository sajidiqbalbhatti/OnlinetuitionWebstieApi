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
    path("", TeacherListView.as_view(), name="teacher-list"),
    
    # Create a teacher profile (only for authenticated teachers)
    path("create/", TeacherCreateView.as_view(), name="teacher-create"),
    
    # Retrieve, update, or delete the logged-in teacher's profile
    path("<int:pk>/", TeacherProfileManageView.as_view(), name="teacher-detail"),
]
