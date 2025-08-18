from django.db import models
from teacher.models import Teacher


class Course(models.Model):
    """
    Model representing a course created by a teacher.
    """
    title = models.CharField(max_length=100, help_text="Title of the course")
    description = models.TextField(help_text="Detailed description of the course")
    tutor = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='courses',
        help_text="The teacher who created this course"
    )
    created = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the course was created")

    class Meta:
        ordering = ['title']  # Default ordering by course title
        verbose_name = "Course"
        verbose_name_plural = "Courses"

    def __str__(self):
        return f"{self.title} - {self.tutor.full_name}"
