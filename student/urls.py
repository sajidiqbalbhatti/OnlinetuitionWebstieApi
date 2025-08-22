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
    path('create/', StudentCreateView.as_view(), name='student_create'),

    # List all students
    path('', StudentListView.as_view(), name='student_list'),

    # Public view of a single student by ID
    # path('<int:pk>/', StudentPublicDetailView.as_view(), name='student_detail'),

    # Manage the logged-in student's own profile (GET, PUT, DELETE)
    path('<int:pk>/', StudentMeView.as_view(), name='student_me'),

    # Enroll logged-in student in a course
    path('enroll/', EnrollCourseView.as_view(), name='student_enroll'),
]
