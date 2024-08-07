from django.db import models
from department.models import Department


class Employee(models.Model):
    """Employee model for adding id, name,department,DOB of employee"""
    employee_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField("date of birth")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """string representation of the object"""
        return f"{self.full_name}({self.employee_id})"

