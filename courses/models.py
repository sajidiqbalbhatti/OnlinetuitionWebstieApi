from django.db import models
from teacher.models import Teacher


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    tutor = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='course')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title