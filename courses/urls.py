from django.urls import path
from .views  import CourseListView, CourseCreateView,CourseDetailView



urlpatterns = [
    path('course/',CourseListView.as_view(),name='course-list'),
    path('course/create/', CourseCreateView.as_view(), name='course-create'),
    path('course/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

]
