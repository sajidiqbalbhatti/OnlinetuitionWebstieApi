from rest_framework import serializers
from .models import Course
from teacher.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying teacher's basic info.
    """
    class Meta:
        model = Teacher
        fields = ['full_name']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for Course model with nested teacher info.
    """
    tutor = TeacherSerializer(read_only=True)  # Nested read-only field

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_at', 'tutor']

    def create(self, validated_data):
        """
        Automatically assign the tutor based on the logged-in user's teacher profile.
        """
        validated_data['tutor'] = self.context['request'].user.teacher_profile
        return super().create(validated_data)
