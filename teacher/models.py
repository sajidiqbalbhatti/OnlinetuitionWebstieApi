from django.db import models
from users.models import User


class Teacher(models.Model):
    """
    Teacher profile linked with a User who has the role 'teacher'.
    Stores personal information and professional qualifications.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
        limit_choices_to={"role": "teacher"},
    )

    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # Professional Information
    bio = models.TextField()
    qualification = models.TextField()

    # Metadata
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self) -> str:
        """Return the teacher's full name as a string representation."""
        return self.full_name

    @property
    def full_name(self) -> str:
        """Return the full name (first + last)."""
        return f"{self.first_name} {self.last_name}".strip()
