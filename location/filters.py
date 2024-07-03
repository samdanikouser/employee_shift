# filters.py
import django_filters
from .models import Locations


class LocationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains',label='Name')

    class Meta:
        model = Locations
        fields = ['name']


