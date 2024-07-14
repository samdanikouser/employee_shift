import django_filters
from .models import EmployeeShift


class EmployeeShiftFilter(django_filters.FilterSet):
    """filter based on name and location name """
    employee_details__full_name = django_filters.CharFilter(lookup_expr='icontains',label='Name')
    location__name = django_filters.CharFilter(lookup_expr='icontains',label='Location')

    class Meta:
        model = EmployeeShift
        fields = ['employee_details__full_name','location__name']


