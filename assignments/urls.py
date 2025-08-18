from django.urls import path
from assignments.views import AssignmentCreateView, AssignmentList, AssignmentDetail

app_name = "assignments"

urlpatterns = [
    path('create/', AssignmentCreateView.as_view(), name='assignment_create'),
    path('list/', AssignmentList.as_view(), name='assignment_list'),
    path('list/<int:pk>/', AssignmentDetail.as_view(), name='assignment_detail'),
]
