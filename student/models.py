from django.db import models
from django.conf import settings
from users.models import User
from courses.models import Course

User = settings.AUTH_USER_MODEL

class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )
    student_name = models.CharField(max_length=100,blank=False,null=False)
    father_name = models.CharField(max_length=100,blank=False,null=False)
    student_class = models.CharField(max_length=50)  # e.g., "10th Grade"
    age = models.IntegerField(null=False, blank=False)
    enrolled_courses = models.ManyToManyField('courses.Course', related_name='students', blank=True)

    def __str__(self):
        return f"{self.student_name} ({self.user.username})"
