# urls.py
from django.urls import path
from student.views import (
    StudentCreateView,
    StudentListView,
    StudentPublicDetailView,
    StudentMeView,
    EnrollCourseView
)

app_name = "student"

urlpatterns = [
    # Create a new student profile
    path('stu/create/', StudentCreateView.as_view(), name='student_create'),

    # List all students
    path('stu/list/', StudentListView.as_view(), name='student_list'),

    # Public view of a single student by ID
    path('stu/list/<int:pk>/', StudentPublicDetailView.as_view(), name='student_detail'),

    # Manage the logged-in student's own profile (GET, PUT, DELETE)
    path('stu/me/', StudentMeView.as_view(), name='student_me'),

    # Enroll logged-in student in a course
    path('stu/enroll/', EnrollCourseView.as_view(), name='student_enroll'),
]
