from django_filters.rest_framework import FilterSet, CharFilter
from reviews.models import Title


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', lookup_expr='icontains')
    category = CharFilter(field_name='category__slug', lookup_expr='icontains')
    name = CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'category', 'genre')
