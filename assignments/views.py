from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from .models import Assignment
from rest_framework.exceptions import PermissionDenied
from .serializer import AssignmentSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

class AssignmentList(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        assignment =Assignment.objects.all()
        serializer =AssignmentSerializer(assignment, many=True)
        return Response(serializer.data)

class AssignmentDetail(APIView):
    permission_classes =[AllowAny]
    def get_object(self, pk):
        try:
            return Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            raise Http404("Course not found for assignment.")
          
    def get(self, request, pk):
        assignment =self.get_object(pk)
        serializer = AssignmentSerializer(assignment)
        return Response(serializer.data)
    
    def put(self, request, pk):
        assignment = self.get_object(pk)
        if assignment.tutor != request.user:
            raise PermissionDenied("You do not have permission to update this assignment.")
        serializer = AssignmentSerializer(assignment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        assignment = self.get_object(pk)
        if assignment.tutor != request.user:
            raise PermissionDenied("You do not have permission to delete this assignment.")
        assignment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssignmentCreateView(APIView):
    permission_classes =[IsAuthenticated]
    
    def post(self, request):
        try:
            teacher_profile = request.user.teacher_profile
        except ObjectDoesNotExist:
           return Response(
          {'detail': "No teacher profile found for this account. Please create a teacher profile before adding assignments."},
          status=status.HTTP_400_BAD_REQUEST
          )
        serializer =AssignmentSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    