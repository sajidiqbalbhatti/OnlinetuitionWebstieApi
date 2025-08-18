from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer
)
from .models import User
from .pagination import MyCursorPagination


# ---------------------------------------------------------------------
# Custom Throttling Classes
# ---------------------------------------------------------------------
class CustomLoginAnonThrottle(AnonRateThrottle):
    """Throttle for anonymous login attempts."""
    scope = 'login'


class CustomLoginUserThrottle(UserRateThrottle):
    """Throttle for authenticated login attempts."""
    scope = 'login'


class CustomRegisterThrottle(AnonRateThrottle):
    """Throttle for user registration attempts."""
    scope = 'register'


# ---------------------------------------------------------------------
# User List API
# ---------------------------------------------------------------------
class UserListView(ListAPIView):
    """
    Returns a list of users with:
    - Cursor Pagination
    - Search (username, role)
    - Ordering (username, role)
    - Filtering (username, role)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    pagination_class = MyCursorPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    search_fields = ['username', 'role']
    ordering_fields = ['username', 'role']
    ordering = ['username']
    filterset_fields = ['username', 'role']


# ---------------------------------------------------------------------
# User Registration API
# ---------------------------------------------------------------------
class RegisterView(APIView):
    """Handles new user registration."""
    permission_classes = [AllowAny]
    throttle_classes = [CustomRegisterThrottle]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------
# User Login API
# ---------------------------------------------------------------------
class LoginView(APIView):
    """Handles user login and returns token + user data."""
    permission_classes = [AllowAny]
    throttle_classes = [CustomLoginAnonThrottle, CustomLoginUserThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'token': token.key,
                    'user': UserSerializer(user).data
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------
# Custom JWT Authentication
# ---------------------------------------------------------------------
class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT Authentication with extra user info."""
    serializer_class = CustomTokenObtainPairSerializer
