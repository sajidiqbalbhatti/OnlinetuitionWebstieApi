# views.py
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import CursorPagination
from rest_framework.throttling import UserRateThrottle
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Teacher
from .serializer import TeacherSerializer
from .filters import TeacherFilter
# ____________cache________
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator




# ----------------------------------------------------------------------
# Custom Scoped Throttling
# ----------------------------------------------------------------------

class CustomTeacherProfileCreateThrottle(UserRateThrottle):
    scope = "teacher_Pro_create"


class CustomTeacherProfileUpdateThrottle(UserRateThrottle):
    scope = "teacher_Pro_update"

# ----------------------------------------------------------------------
# Teacher Create API
# ----------------------------------------------------------------------
from .permissions import IsTeacher
class TeacherCreateView(APIView):
    """
    Allows authenticated teachers to create their profile.
    Only one profile per teacher is allowed.
    """

    permission_classes = [IsAuthenticated,IsTeacher]
    throttle_classes = [CustomTeacherProfileCreateThrottle]

    def post(self, request):
        
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
@method_decorator(cache_page(60*3),name='dispatch')
class TeacherListView(generics.ListAPIView):
    """
    Public endpoint: List all teachers.
    Supports pagination, filtering, searching, and ordering.
    """

    queryset = Teacher.objects.select_related('user')
    serializer_class = TeacherSerializer
    permission_classes = [AllowAny]
    pagination_class = CursorPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = TeacherFilter
    search_fields = ["first_name", "last_name", "qualification"]
    
    def get_queryset(self):
        print("DB query is working")
        return super().get_queryset()
    # __lowLevelCache_____
    # def get_queryset(self):
    #     teacher_list = cache.get('teacher_list')
        
    #     if not teacher_list:
    #         print("Cache Miss fetching from DB")
    #         teacher_list=Teacher.objects.select_related('user')
    #         cache.set('teacher_list', teacher_list, timeout=60*1)
    #     else:
    #         print('Cache hit')
    #     return teacher_list
  

# ----------------------------------------------------------------------
# Teacher Profile Manage API
# ----------------------------------------------------------------------
class TeacherProfileManageView(generics.RetrieveUpdateDestroyAPIView):
    """
    Logged-in teacher can view, update, or delete their profile.
    """
    queryset =Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacher]
    throttle_classes = [CustomTeacherProfileUpdateThrottle]

    def get_throttles(self):
        """
        Disable throttling for PUT requests.
        """
        if self.request.method.lower() == "put":
            return []
        return super().get_throttles()

    