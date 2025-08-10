from django.urls import path

from teacher.views import *
urlpatterns = [
   # urls.py
         path('pro/',TeacherListView.as_view(),name='teacher'),
         path('pro/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
         path('pro/<int:pk>',TeacherProfileManageView.as_view()),
         path('pro/create/', TeacherCreateView.as_view(), name='teacher-create'),


]
