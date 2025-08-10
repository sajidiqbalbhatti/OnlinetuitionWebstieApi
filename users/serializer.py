from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email','role']
    
class RegisterSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False) 
    class Meta:
        model = User
        fields = ['username','email','password','role','is_staff']
        extra_kwargs = {'password':{'write_only':True}}
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password too short. ")
        return value
    
    def validate(self, data):
       email = data.get('email')
       if email and User.objects.filter(email=email).exists():
          raise serializers.ValidationError({'email': "Email already exists"})
       return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password =serializers.CharField()
    
    def validate(self, data):
        user =authenticate(**data)
        if user and user.is_active:
            return user
        
        raise serializers.ValidationError("Invalid Credentials")