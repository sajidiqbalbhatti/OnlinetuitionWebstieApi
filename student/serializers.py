# serializers.py
from rest_framework import serializers
from .models import Student
from courses.models import Course
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for basic User info (nested in Student)."""
    class Meta:
        model = User
        fields = ['username', 'email']


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course info (nested in Student)."""
    class Meta:
        model = Course
        fields = ['id', 'title', 'description']  # jo fields chahiye wo add karen


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for Student model.
    Handles nested user info and enrolled courses.
    """
    user = UserSerializer(read_only=True)  # Nested user info
    enrolled_courses = CourseSerializer(many=True, read_only=True)  # Nested courses info

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
