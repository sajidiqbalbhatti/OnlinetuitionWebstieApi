# views.py
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import CursorPagination
from rest_framework.throttling import UserRateThrottle
from .models import Student
from .serializers import StudentSerializer
from .filter import StudentAgeFilter
# ______Cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page




# ----------------------------------------------------------------------
# Custom Throttling Classes for Student
# ----------------------------------------------------------------------
class StudentCreateThrottle(UserRateThrottle):
    scope = "student_create"


class StudentUpdateThrottle(UserRateThrottle):
    scope = "student_update"


# ----------------------------------------------------------------------
# Student Create API
# ----------------------------------------------------------------------
class StudentCreateView(APIView):
    """
    Allows authenticated students to create their profile.
    Only one profile per student is allowed.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [StudentCreateThrottle]

    def post(self, request):
        if request.user.role != "student":
            return Response(
                {"error": "Only students can create a student profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if hasattr(request.user, "student"):
            return Response(
                {"error": "Profile already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["user"] = request.user.id

        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------
# Student List API
# ----------------------------------------------------------------------
@method_decorator(cache_page(60*2),name='dispatch')
class StudentListView(generics.ListAPIView):
    """
    Public endpoint to list all students.
    Supports filtering, searching, ordering, and cursor pagination.
    """
  
    queryset = Student.objects.prefetch_related('enrolled_courses__tutor')
    serializer_class = StudentSerializer
    permission_classes = [AllowAny]
    pagination_class = CursorPagination
    filterset_class = StudentAgeFilter

    ordering_fields = ["student_name", "age"]
    search_fields = ["student_name", "age", "student_class"]
    
    def get_queryset(self):
        print("DB Query executed")
        return super().get_queryset()
    # ________low level Cache_______

    # def get_queryset(self):
    #     student_list =cache.get('student_list')
        
    #     if not student_list:
    #         print("Db use")
    #         student_list = Student.objects.prefetch_related('enrolled_courses__tutor')
    #         cache.set('student_list', student_list, 60*1)
    #     else:
    #       print('use cache')
    #     return student_list


# ----------------------------------------------------------------------
# Logged-in Student Profile Management
# ----------------------------------------------------------------------

from .permission import IsStudent
class StudentMeView(APIView):
    """
    Logged-in student can retrieve, update, or delete their profile.
    """

    permission_classes = [IsStudent]
    throttle_classes = [StudentUpdateThrottle]

    def get_throttles(self):
        """Disable throttling for PUT requests."""
        if self.request.method.lower() == "put":
            return []
        return super().get_throttles()

    def get(self, request,pk):
        student = get_object_or_404(Student, pk=pk)
        # if student!==:
        #     return Response({"error": "Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentSerializer(student)
        return Response(serializer.data)

    def put(self, request,pk):
        student = get_object_or_404(Student, pk=pk)
        # if not student:
        #     return Response({"error": "Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        self.check_object_permissions(request, student)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk):
        student = get_object_or_404(Student,pk=pk)
        self.check_object_permissions(request,student)
        student.delete()
        return Response({"message": "Profile deleted successfully."}, status=status.HTTP_200_OK)


# ----------------------------------------------------------------------
# Enroll Student in a Course
# ----------------------------------------------------------------------
class EnrollCourseView(APIView):
    """
    Allows a logged-in student to enroll in a course.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        student = getattr(request.user, "student", None)
        if not student:
            return Response({"error": "Profile does not exist."}, status=status.HTTP_404_NOT_FOUND)

        course_id = request.data.get("course_id")
        if not course_id:
            return Response({"error": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student.enrolled_courses.add(course_id)
            return Response({"message": "Successfully enrolled in course."})
        except Exception:
            return Response({"error": "Invalid Course ID."}, status=status.HTTP_400_BAD_REQUEST)
