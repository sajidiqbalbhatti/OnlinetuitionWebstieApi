# urls.py
from django.urls import path
from .views import CourseListView, CourseCreateView, CourseDetailView

app_name = "courses"  # optional, recommended for namespacing

urlpatterns = [
    # List all courses
    path("course/", CourseListView.as_view(), name="course-list"),

    # Create a new course (teacher only)
    path("course/create/", CourseCreateView.as_view(), name="course-create"),

    # Retrieve, update, or delete a specific course by ID
    path("course/<int:pk>/", CourseDetailView.as_view(), name="course-detail"),
]
