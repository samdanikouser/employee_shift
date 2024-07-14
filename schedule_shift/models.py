from django.db import models

from department.models import Department
from employee.models import Employee
from location.models import Locations


class EmployeeShift(models.Model):
    """Shift model for storing the shift details of employee"""
    id = models.AutoField(primary_key=True)
    employee_details = models.ForeignKey(Employee, on_delete=models.CASCADE)
    location = models.ForeignKey(Locations, on_delete=models.CASCADE)
    date = models.DateField("shift from date")
    from_time = models.TimeField("shift timing")
    to_time = models.TimeField("shift to date")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """string representation of the object"""
        return f'{self.employee_details} - {self.date}'

