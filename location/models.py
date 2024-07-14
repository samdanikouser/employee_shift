from django.db import models


class Locations(models.Model):
    """Location model for adding location name"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """string representation of the object"""
        return f"{self.name}"
