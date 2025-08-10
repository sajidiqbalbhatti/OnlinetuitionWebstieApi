from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import RegisterSerializer , LoginSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated

# Create your views here.

class RegisterView(APIView):
   permission_classes = [AllowAny]
   def post(self, request):
       serializer = RegisterSerializer(data=request.data)
       if serializer.is_valid():
           user = serializer.save()
           token, _=Token.objects.get_or_create(user=user)
           return Response({'token':token.key,'user':UserSerializer(user).data}, status=201)
       return Response(serializer.errors, status=400)

class LoginView(APIView):
    permission_classes =[AllowAny]
    def post(self, request):
        serializer =LoginSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data
            token,_ = Token.objects.get_or_create(user=user)
            return Response({'token':token.key,'user':UserSerializer(user).data})
        return Response(serializer.errors, status=400)