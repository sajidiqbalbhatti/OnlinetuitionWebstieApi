# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status,generics
from .models import Teacher

from .serializer import TeacherSerializer

class TeacherCreateView(APIView):
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        if request.user.role !='teacher':
            return Response({'error':'Only teachers can create a teacher profile'})
        
        if hasattr(request.user,'teacher'):
            return Response({'error':'Teacher profile already exists.'},status=400)
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = TeacherSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TeacherListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TeacherDetailView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request, pk, *args, **kwargs):
        try:
            teacher = Teacher.objects.get(pk=pk)
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher not found."}, status=status.HTTP_404_NOT_FOUND)


class TeacherProfileManageView(generics.RetrieveUpdateDestroyAPIView):
    """
    Only logged-in teacher can manage their profile
    """
    serializer_class = TeacherSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.teacher
        except Teacher.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        teacher = self.get_object()
        if teacher is None:
            return Response({"detail": "You are not registered as a teacher."}, status=status.HTTP_403_FORBIDDEN)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        teacher = self.get_object()
        if teacher is None:
            return Response({"detail": "You are not registered as a teacher."}, status=status.HTTP_403_FORBIDDEN)
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        teacher = self.get_object()
        if teacher is None:
            return Response({"detail": "You are not registered as a teacher."}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)