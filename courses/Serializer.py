from rest_framework import serializers
from .models import Course
from teacher.models import Teacher
# from teacher.serializer import TeacherSerializer

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields =['full_name']

class CourseSerializer(serializers.ModelSerializer):
    tutor =TeacherSerializer(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['created_at','tutor']
    
    def create(self, validated_data):
        validated_data['tutor'] = self.context['request'].user.teacher_profile
        return super().create(validated_data)