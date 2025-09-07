# models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Student(models.Model):
    """
    Represents a student profile linked to a User account with role='student'.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        help_text="Linked user account with role='student'."
    )
    student_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Full name of the student."
    )
    father_name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        help_text="Father's name of the student."
    )
    student_class = models.CharField(
        max_length=50,
        blank=True,
        help_text="Class/grade of the student, e.g., '10th Grade'."
    )
    age = models.PositiveIntegerField(
        blank=False,
        null=False,
        help_text="Age of the student."
    )
    created = models.DateTimeField(
        auto_now_add=True,
        help_text="Profile creation timestamp."
    )
    enrolled_courses = models.ManyToManyField(
        'courses.Course',
        related_name='students',
        blank=False,
        null=False,
        help_text="Courses the student is enrolled in."
    )

    def __str__(self):
        return f"{self.student_name} ({self.user.username})"
