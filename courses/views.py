from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.permissions import IsAuthenticated,AllowAny

from .models import Course
from .Serializer import CourseSerializer

# Create your views here
class CourseListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)
        
class CourseCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            teacher = request.user.teacher_profile
        except:
            return Response({"detail":"Only  teacher can create courses."})
        serializer = CourseSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(tutor=teacher)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CourseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None
        
    def get(self, request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response({"detail": "Course not found."}, status=404)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    
    def put(self, request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response({"detail":"course not found."}, status=404)
        
        try:
            if course.tutor !=request.user.teacher:
                return  Response({"detail":"You do not have  permission to update"})
        except:
            return Response({"detail":"Only teachers can update courses."})
        
        serializer = CourseSerializer(course, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    
    def delete(self, request, pk):
        course = self.get_object(pk)
        if course is None:
            return Response({"detail": "Course not found."}, status=404)

        try:
            if course.tutor != request.user.teacher:
                return Response({"detail": "You do not have permission to delete this course."}, status=403)
        except:
            return Response({"detail": "Only teachers can delete courses."}, status=403)

        course.delete()
        return Response({"detail": "Course deleted successfully."}, status=204)
    