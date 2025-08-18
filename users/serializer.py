# serializers.py

from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


# ---------------------------------------------------------------------
# User Serializer
# ---------------------------------------------------------------------
class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic user representation."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]


# ---------------------------------------------------------------------
# User Registration Serializer
# ---------------------------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    """Handles user registration with validation."""

    is_staff = serializers.BooleanField(default=False)

    class Meta:
        model = User
        fields = ["username", "email", "password", "role", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value):
        """Validate password strength."""
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long.")
        return value

    def validate(self, data):
        """Check if email already exists."""
        email = data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        return data

    def create(self, validated_data):
        """Create a new user with hashed password."""
        return User.objects.create_user(**validated_data)


# ---------------------------------------------------------------------
# User Login Serializer
# ---------------------------------------------------------------------
class LoginSerializer(serializers.Serializer):
    """Handles user login validation."""

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Authenticate user credentials."""
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid username or password.")


# ---------------------------------------------------------------------
# Custom JWT Serializer
# ---------------------------------------------------------------------
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Authentication:
    Requires email along with username & password.
    Returns access & refresh tokens with user details.
    """

    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")
        email = attrs.get("email")

        if not username or not password or not email:
            raise serializers.ValidationError("Username, password, and email are required.")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid username or password.")
        if user.email != email:
            raise serializers.ValidationError("Email does not match this user.")

        # Let SimpleJWT handle token generation
        data = super().validate(attrs)
        data.update({
            "role": user.role,
            "email": user.email,
        })
        return data
