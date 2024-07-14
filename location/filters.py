# filters.py
import django_filters
from .models import Locations


class LocationFilter(django_filters.FilterSet):
    """used to filter the location by fields(name) in the table view"""
    name = django_filters.CharFilter(lookup_expr='icontains',label='Name')

    class Meta:
        """specifies the model on which the filters operate and
                the list of fields from which filter can be applied"""
        model = Locations
        fields = ['name']


