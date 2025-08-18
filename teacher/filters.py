# filters.py
import django_filters
from .models import Teacher


class TeacherFilter(django_filters.FilterSet):
    """
    FilterSet for Teacher model.
    Supports case-insensitive search on first name, last name, and qualification.
    """

    first_name = django_filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )
    last_name = django_filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )
    qualification = django_filters.CharFilter(
        field_name="qualification", lookup_expr="icontains"
    )

    class Meta:
        model = Teacher
        fields = ["first_name", "last_name", "qualification"]
