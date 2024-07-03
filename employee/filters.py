# filters.py
import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    employee_id = django_filters.NumberFilter(lookup_expr='icontains',label='Id')
    full_name = django_filters.CharFilter(lookup_expr='icontains',label='Name')
    department = django_filters.CharFilter(lookup_expr='icontains',label='department')
    date_of_birth = django_filters.CharFilter(lookup_expr='icontains',label='DOB')

    class Meta:
        model = Employee
        fields = ['employee_id', 'full_name', 'department', 'date_of_birth']


