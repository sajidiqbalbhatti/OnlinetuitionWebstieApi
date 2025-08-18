from rest_framework import serializers
from .models import Assignment
from courses.models import Course

class AssignmentSerializer(serializers.ModelSerializer):
    tutor_name = serializers.CharField(
        source='course.tutor.full_name', 
        read_only=True
    )
    course_name = serializers.CharField(
        source='course.title', 
        read_only=True
    )

    class Meta:
        model = Assignment
        fields = [
            'title',
            'course',
            'description',
            'due_date',
            'tutor_name',
            'course_name'
        ]

    def validate_course(self, course):
        """
        Ensure that only teachers can create assignments for their own courses.
        """
        user = self.context['request'].user

        if user.role.lower() != 'teacher':
            raise serializers.ValidationError("Only teachers can create assignments.")

        if course.tutor != user.teacher_profile:
            raise serializers.ValidationError(
                "You are not allowed to create an assignment for this course."
            )

        return course

    def create(self, validated_data):
        """
        Set the tutor automatically based on the logged-in user.
        """
        validated_data['tutor'] = self.context['request'].user
        return super().create(validated_data)
