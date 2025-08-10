from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Student
from .serializers import StudentSerializer
# Create your views here.    
class StudentCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if hasattr(request.user, 'student'):
            return Response({'error':'Profile already exists.'},status=400)
        data = request.data.copy()
        data['user']=request.user.id
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)  
    
class StudentListView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        student =Student.objects.all()
        serializer =StudentSerializer(student, many=True)
        return Response(serializer.data)
    
class StudentPublicDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
    
class StudentMeView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request):
        if not hasattr(request.user, 'student'):
            return Response({'error':'Profile does not exist.'},status=404)
        serializer = StudentSerializer(request.user.student)
        return Response(serializer.data)
    
    def put(self, request):
        student = request.user.student
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    
    def delete(self, request):
        student = request.user.student
        student.delete()
        return Response({'message':'Profile deleted successfully'}, status=200)
        
    

class EnrollCourseView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        student = request.user.student
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error':'Course ID is required.'}, status=400)
        
        try:
            student.enrolled_courses.add(course_id)
            return Response({'message':'Successfully enrolled in course.'})
        except:
            return Response ({'error':'Invalid Course ID'}, status=400)
                      