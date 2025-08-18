# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import CursorPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course
from .Serializer import CourseSerializer
from .filters import CourseFilter


# ---------------------------
# Custom Throttling Classes
# ---------------------------
class CourseListThrottle(AnonRateThrottle):
    scope = 'course_list'


class CourseCreateThrottle(UserRateThrottle):
    scope = 'course_create'


class CourseUpdateThrottle(UserRateThrottle):
    scope = 'course_update'


# ---------------------------
# Course List API
# ---------------------------
class CourseListView(generics.ListAPIView):
    """
    Returns a list of courses with support for:
    - Cursor pagination
    - Search by title, description, tutor names
    - Ordering by title
    - Filtering by title or tutor
    """
    permission_classes = [AllowAny]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CursorPagination
    throttle_classes = [CourseListThrottle]
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'tutor']
    ordering_fields = ['title']
    ordering = ['title']
    search_fields = [
        'title',
        'description',
        'tutor__first_name',
        'tutor__last_name'
    ]
    # filterset_class = CourseFilter  # Optional


# ---------------------------
# Course Create API
# ---------------------------
class CourseCreateView(APIView):
    """
    Allows teachers to create courses
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [CourseCreateThrottle]

    def post(self, request):
        try:
            teacher = request.user.teacher_profile
        except AttributeError:
            return Response({"detail": "Only teachers can create courses."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(tutor=teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------
# Course Detail / Update / Delete API
# ---------------------------
class CourseDetailView(APIView):
    """
    Retrieve, update, or delete a course.
    Only the course's tutor can update or delete.
    """
    permission_classes = [IsAuthenticated]

    def get_throttles(self):
        if self.request.method == 'PUT':
            return [CourseUpdateThrottle()]
        return super().get_throttles()

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check teacher permission
        try:
            if course.tutor != request.user.teacher_profile:
                return Response({"detail": "You do not have permission to update this course."}, status=status.HTTP_403_FORBIDDEN)
        except AttributeError:
            return Response({"detail": "Only teachers can update courses."}, status=status.HTTP_403_FORBIDDEN)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check teacher permission
        try:
            if course.tutor != request.user.teacher_profile:
                return Response({"detail": "You do not have permission to delete this course."}, status=status.HTTP_403_FORBIDDEN)
        except AttributeError:
            return Response({"detail": "Only teachers can delete courses."}, status=status.HTTP_403_FORBIDDEN)

        course.delete()
        return Response({"detail": "Course deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
