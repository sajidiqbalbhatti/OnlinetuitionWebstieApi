from rest_framework import serializers
from .models import Teacher
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic User info."""

    class Meta:
        model = User
        fields = ["username", "email"]
        read_only_fields = ["username", "email"]


class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for Teacher model with nested User info."""

    user = UserSerializer(read_only=True)
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Teacher
        fields = [
            "id",
            "user",
            "first_name",
            "last_name",
            "full_name",
            "bio",
            "qualification",
        ]
        read_only_fields = ["id", "user", "full_name"]

    def validate_first_name(self, value: str) -> str:
        """Ensure first name is not empty."""
        if not value.strip():
            raise serializers.ValidationError("First name is required.")
        return value

    def validate_last_name(self, value: str) -> str:
        """Ensure last name is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Last name is required.")
        return value
