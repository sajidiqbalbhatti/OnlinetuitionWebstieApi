from django.urls import path
from student.views import StudentCreateView,StudentListView,StudentPublicDetailView,StudentMeView,EnrollCourseView



urlpatterns = [
    path('stu/create/', StudentCreateView.as_view(), name='student_create'),
    path('stu/list/',StudentListView.as_view(),name='student_list'),
    path('stu/<int:pk>/',StudentPublicDetailView.as_view(), name='stu_detail'),
    path('stu/me/',StudentMeView.as_view(), name='student_curd'),
    path('stu/enroll/', EnrollCourseView.as_view()),
 
]
