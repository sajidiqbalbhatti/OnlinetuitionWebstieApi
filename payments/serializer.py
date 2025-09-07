from rest_framework import serializers
from .models import Payment
from courses.models import Course
from users.models import User



# # User serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["username", "email"]  

# # ___CourseSerializer 
# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model  = Course
#         fields = ['title','price']



class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username",read_only=True)
    course = serializers.CharField(source="course.title",read_only=True)
    
    class Meta:
        model = Payment
        fields = [
             "id",
            "stripe_payment_intent",
            "stripe_session_id",
            "amount",
            "currency",
            "status",
            "created",
            "user",      # full user object
            "course"
        ]
