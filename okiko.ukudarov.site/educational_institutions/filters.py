import django_filters
from .models import University


class UniversityFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = University
        fields = {'title': ['icontains']}
