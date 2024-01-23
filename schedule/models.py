from django.db import models

from employee.models import Employee
from location.models import Location


# Create your models here.

class Scheduler(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,error_messages={"employee": "Select the employee"})
    location = models.ForeignKey(Location, on_delete=models.CASCADE,error_messages={"location": "Select the location"})
    date = models.DateField("shift from date",error_messages={"date": "Shift date is mandatory"})
    from_time = models.TimeField("shift from time",error_messages={"from_time": "from time required"})
    to_time = models.TimeField("shift to time",error_messages={"to_time": "to time require"})
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee}"
