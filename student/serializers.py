# serializers.py
from rest_framework import serializers
from .models import Student
from courses.models import Course
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic User info (nested in Student)."""
    
    class Meta:
        model = User
        fields = ['username']


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model.
    Handles nested user info and course enrollment.
    """
    user = UserSerializer(read_only=True)  # Nested user info, read-only
    enrolled_courses = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Course.objects.all(),
        required=False,
        help_text="List of course IDs the student is enrolled in."
    )

    class Meta:
        model = Student
        fields = [
            'id',
            'user',
            'student_name',
            'father_name',
            'student_class',
            'enrolled_courses',
            'age'
        ]
        read_only_fields = ['user']
