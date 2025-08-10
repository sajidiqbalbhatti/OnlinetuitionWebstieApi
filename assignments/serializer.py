from rest_framework import serializers
from .models import Assignment
from courses.models import Course

class AssignmentSerializer(serializers.ModelSerializer):
    tutor_name=serializers.CharField(source='course.tutor.full_name', read_only=True)
    course_name=serializers.CharField(source='course.title', read_only=True)
    # tutor = serializers.ReadOnlyField(source='tutor.full_name')
    # course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), write_only=True)

    class Meta:
        model =Assignment
        fields = [ 'title', 'course','description', 'due_date', 'tutor_name', 'course_name']

    def validate_course(self, course):
        user =self.context['request'].user
        if user.role.lower() !='teacher':
            raise serializers.ValidationError("Only teacher can create assignments.")
        if course.tutor != user.teacher_profile:

            raise serializers.ValidationError("You are not allowed to create an assignment for this course.")                            
        return course
    
    def create(self, validated_data):
        
        validated_data['tutor']= self.context['request'].user
        return super().create(validated_data)