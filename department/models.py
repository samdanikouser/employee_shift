from django.db import models


class Department(models.Model):
    """Department model for adding department name of employee"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """string representation of the object"""
        return f"{self.name}"
