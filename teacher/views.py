# views.py
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import CursorPagination
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend

from .models import Teacher
from .serializer import TeacherSerializer
from .filters import TeacherFilter


# ----------------------------------------------------------------------
# Custom Scoped Throttling
# ----------------------------------------------------------------------
class CustomTeacherProfileCreateThrottle(UserRateThrottle):
    scope = "teacher_profile_create"


class CustomTeacherProfileUpdateThrottle(UserRateThrottle):
    scope = "teacher_profile_update"


# ----------------------------------------------------------------------
# Teacher Create API
# ----------------------------------------------------------------------
class TeacherCreateView(APIView):
    """
    Allows authenticated teachers to create their profile.
    Only one profile per teacher is allowed.
    """

    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomTeacherProfileCreateThrottle]

    def post(self, request):
        if request.user.role != "teacher":
            return Response(
                {"error": "Only teachers can create a teacher profile."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if hasattr(request.user, "teacher_profile"):
            return Response(
                {"error": "Teacher profile already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = request.data.copy()
        data["user"] = request.user.id

        serializer = TeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ----------------------------------------------------------------------
# Teacher List API
# ----------------------------------------------------------------------
class TeacherListView(generics.ListAPIView):
    """
    Public endpoint: List all teachers.
    Supports pagination, filtering, searching, and ordering.
    """

    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]
    pagination_class = CursorPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = TeacherFilter
    search_fields = ["first_name", "last_name", "qualification"]


# ----------------------------------------------------------------------
# Teacher Profile Manage API
# ----------------------------------------------------------------------
class TeacherProfileManageView(generics.RetrieveUpdateDestroyAPIView):
    """
    Logged-in teacher can view, update, or delete their profile.
    """

    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [CustomTeacherProfileUpdateThrottle]

    def get_throttles(self):
        """
        Disable throttling for PUT requests.
        """
        if self.request.method.lower() == "put":
            return []
        return super().get_throttles()

    def get_object(self):
        """
        Returns teacher profile of the logged-in user.
        """
        return getattr(self.request.user, "teacher_profile", None)

    def get(self, request, *args, **kwargs):
        teacher = self.get_object()
        if not teacher:
            return Response(
                {"detail": "You are not registered as a teacher."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        teacher = self.get_object()
        if not teacher:
            return Response(
                {"detail": "You are not registered as a teacher."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        if not teacher:
            return Response(
                {"detail": "You are not registered as a teacher."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return self.destroy(request, *args, **kwargs)
