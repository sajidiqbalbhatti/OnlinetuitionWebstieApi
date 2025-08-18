# filter.py
import django_filters
from .models import Student


class StudentAgeFilter(django_filters.FilterSet):
    """
    FilterSet for Student model to allow filtering by:
    - Age range (gte / lte)
    - Partial student name match
    - Partial enrolled course title match
    """
    age_gt = django_filters.NumberFilter(
        field_name='age',
        lookup_expr='gte',
        label='Minimum Age'
    )
    age_lt = django_filters.NumberFilter(
        field_name='age',
        lookup_expr='lte',
        label='Maximum Age'
    )
    student_name = django_filters.CharFilter(
        field_name='student_name',
        lookup_expr='icontains',
        label='Student Name'
    )
    enrolled_courses = django_filters.CharFilter(
        field_name='enrolled_courses__title',
        lookup_expr='icontains',
        label='Enrolled Course Title'
    )

    class Meta:
        model = Student
        fields = ['age_gt', 'age_lt', 'student_name', 'enrolled_courses']
