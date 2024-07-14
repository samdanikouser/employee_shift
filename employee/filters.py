import django_filters
from .models import Employee


class EmployeeFilter(django_filters.FilterSet):
    """used to filter the employee by fields(id,name,department,DOB) in the table view"""
    employee_id = django_filters.NumberFilter(lookup_expr='icontains', label='Id')
    full_name = django_filters.CharFilter(lookup_expr='icontains', label='Name')
    department__name = django_filters.CharFilter(lookup_expr='icontains', label='department')
    date_of_birth = django_filters.CharFilter(lookup_expr='icontains', label='DOB')

    class Meta:
        """specifies the model on which the filters operate and
        the list of fields from which filter can be applied"""
        model = Employee
        fields = ['employee_id', 'full_name', 'department', 'date_of_birth']
