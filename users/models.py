from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Adds a `role` field to differentiate between Admin, Teacher, and Student.
    """

    class Roles(models.TextChoices):
        ADMIN = "admin", "Admin"
        TEACHER = "teacher", "Teacher"
        STUDENT = "student", "Student"

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.STUDENT,
    )

    def __str__(self) -> str:
        """Return a readable string representation of the user."""
        return f"{self.username} ({self.get_role_display()})"
