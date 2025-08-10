from rest_framework import serializers
from .models import Student
from courses.models import Course
from users.models import User


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model=User
    fields =['username']

class StudentSerializer(serializers.ModelSerializer):
    enrolled_courses = serializers.PrimaryKeyRelatedField(
      many=True , queryset =Course.objects.all(),
      required=False
    )
    user =UserSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ['id','user','student_name','father_name','student_class','enrolled_courses','age']
        read_only_fields = ['user']