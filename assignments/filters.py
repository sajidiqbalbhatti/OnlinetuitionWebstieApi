import django_filters
from .models import Assignment


class AssignmentFilter(django_filters.FilterSet):
    tutor = django_filters.CharFilter(
        field_name='tutor__username',
        lookup_expr='icontains'
    )
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains'
    )
    course = django_filters.CharFilter(
        field_name='course__title',
        lookup_expr='icontains'
    )

    class Meta:
        model = Assignment
        fields = ['tutor', 'title', 'course']
