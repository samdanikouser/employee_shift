from django.contrib.auth.models import User
from django.db import models

from department.models import Department


# Create your models here.

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200, error_messages={"name": "Name required"})
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null=True,
                                   error_messages={"department": "Name required"})
    date_of_birth = models.DateField("date of birth", error_messages={"dob": "DOB required"},null=True)
    enrollment_status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name}"


class Enrollment(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    photo = models.FileField(null=True, upload_to="photos")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee}"
