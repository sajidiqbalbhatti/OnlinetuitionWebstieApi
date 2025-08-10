from django.db import models
from users.models import User

class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'role': 'teacher'}
    )
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    bio = models.TextField(blank=False, null=False)
    qualification = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        first = self.first_name or ''
        last = self.last_name or ''
        return f"{first} {last}".strip()
