import django_filters
from .models import Course


class CourseFilter(django_filters.FilterSet):
    """
    Filter for searching and filtering Course instances.
    Supports filtering by course title and tutor's first and last names.
    """
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Course Title',
        help_text='Filter courses by title (case-insensitive, partial match)'
    )
    tutor_first = django_filters.CharFilter(
        field_name='tutor__first_name',
        lookup_expr='icontains',
        label='Tutor First Name',
        help_text='Filter courses by tutor’s first name (case-insensitive, partial match)'
    )
    tutor_last = django_filters.CharFilter(
        field_name='tutor__last_name',
        lookup_expr='icontains',
        label='Tutor Last Name',
        help_text='Filter courses by tutor’s last name (case-insensitive, partial match)'
    )

    class Meta:
        model = Course
        fields = ['title', 'tutor_first', 'tutor_last']
