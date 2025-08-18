from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.pagination import CursorPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import BaseThrottle
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend

from .models import Assignment
from .serializer import AssignmentSerializer
from .filters import AssignmentFilter
import random


# -------------------------------
# Custom Random Throttle
# -------------------------------
class RandomRateThrottle(BaseThrottle):
    """
    Randomly allows or denies a request (for demonstration purposes).
    """
    def allow_request(self, request, view):
        return random.randint(1, 5) != 1


# -------------------------------
# Assignment List View
# -------------------------------
class AssignmentList(ListAPIView):
    """
    Retrieve a paginated list of assignments with filtering, searching, and ordering.
    """
    permission_classes = [AllowAny]
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    pagination_class = CursorPagination
    throttle_classes = [RandomRateThrottle]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AssignmentFilter

    ordering_fields = ['title']
    search_fields = ['title', 'course__title', 'tutor__username']


# -------------------------------
# Assignment Detail View
# -------------------------------
class AssignmentDetail(APIView):
    """
    Retrieve, update, or delete an assignment.
    Only the tutor who created the assignment can update or delete it.
    """
    permission_classes = [AllowAny]

    def get_object(self, pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404("Course not found for assignment.")

    def get(self, request, pk):
        assignment = self.get_object(pk)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    def put(self, request, pk):
        assignment = self.get_object(pk)
        if assignment.tutor != request.user:
            raise PermissionDenied("You do not have permission to update this assignment.")

        serializer = AssignmentSerializer(assignment, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        assignment = self.get_object(pk)
        if assignment.tutor != request.user:
            raise PermissionDenied("You do not have permission to delete this assignment.")

        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------
# Assignment Create View
# -------------------------------
class AssignmentCreateView(APIView):
    """
    Create a new assignment.
    Only authenticated teachers with a profile can create assignments.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            teacher_profile = request.user.teacher_profile
        except ObjectDoesNotExist:
            return Response(
                {"detail": "No teacher profile found. Create a teacher profile before adding assignments."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AssignmentSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
