from django.db import models

# Create your models here.
from django.db import models
from courses.models import Course
from users.models import User
from student.models import Student


class Assignment(models.Model):
    tutor =models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role':'teacher'})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments')
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
   
    def __str__(self):
        return f"{self.title} - {self.course.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    grade = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.assignment.title}"
