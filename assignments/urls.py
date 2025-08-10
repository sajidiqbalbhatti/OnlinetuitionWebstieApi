from django.urls import path
from assignments.views import AssignmentCreateView,AssignmentList,AssignmentDetail



urlpatterns = [
    path('create/',AssignmentCreateView.as_view(),name='assignment'),
    path('list/',AssignmentList.as_view(), name='assignment_list'),
    path('list/<int:pk>/',AssignmentDetail.as_view(), name='assignment_list'),
]
