from django_filters import rest_framework as filters
from .models import Job


class JobFilter(filters.FilterSet):
    keyword = filters.CharFilter(field_name="title", lookup_expr='icontains')  # for search
    location = filters.CharFilter(field_name="search", lookup_expr='icontains')  # for search

    min = filters.NumberFilter(field_name="salary" or 0, lookup_expr='gte')  # for salary range
    max = filters.NumberFilter(field_name="salary" or 1000000000, lookup_expr='lte')

    class Meta:
        model = Job
        fields = ['keyword', 'location', 'education', 'job_type', 'experience', 'min', 'max']
