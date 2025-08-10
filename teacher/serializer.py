from rest_framework import serializers
from .models import Teacher
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
                        

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Nested user info
    full_name = serializers.ReadOnlyField()  # From model property
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Teacher
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'bio',
            'qualification',
        ]
        read_only_fields = ['id', 'user', 'full_name', 'email']

    def validate_first_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("First name is required.")
        return value

    def validate_last_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Last name is required.")
        return value
