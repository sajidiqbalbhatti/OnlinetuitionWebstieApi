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
from .permission import IsTeacherOrReadOnly
import random
# ______Low Level Cache_________
from django.core.cache import cache




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
    queryset = Assignment.objects.select_related('course', 'tutor')
    serializer_class = AssignmentSerializer
    pagination_class = CursorPagination
    throttle_classes = [RandomRateThrottle]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AssignmentFilter

    ordering_fields = ['title']
    search_fields = ['title', 'course__title', 'tutor__username']
    
    def get_queryset(self):
        assignment_list=cache.get('assignment')
        print("cache is working ")
        if not assignment_list:
            print("cache is not working")
            assignment_list= Assignment.objects.select_related('course', 'tutor')
            cache.set('assignment',assignment_list,timeout=60*1)
        
        return assignment_list

# -------------------------------
# Assignment Detail View
# -------------------------------
class AssignmentDetail(APIView):
    """
    Retrieve, update, or delete an assignment.
    Only the tutor who created the assignment can update or delete it.
    """
    permission_classes = [AllowAny]
    permission_classes=[IsTeacherOrReadOnly]
    
    

    def get_object(self, pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404("Assignment Not Found.")

    def get(self, request, pk):
        cache_key = f"assignment_{pk}"
        assignment = cache.get(cache_key)
        if assignment:
            print('cache is working')
        else:
            print("DB is working")
            try:
               assignment =Assignment.objects.get(pk=pk)
               cache.set(cache_key ,assignment,timeout=60*10)
           
            except Assignment.DoesNotExist:
                 
                return Response({"detail":"Assignment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)

    def put(self, request, pk):
        assignment = self.get_object(pk)
        # __add the custom permission
        self.check_object_permissions(request, assignment)
        serializer = AssignmentSerializer(assignment, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # Cache delete
        cache.delete(f"assignment_{pk}")
        return Response(serializer.data)

    def delete(self, request, pk):
        assignment = self.get_object(pk)
        # _____add the custom permission
        self.check_object_permissions(request, assignment)
        assignment.delete()
        # Cache delete
        cache.delete(f"assignment_{pk}")
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
