from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Registered employee model to display in django admin with filter option
     and fields to display on list"""
    list_filter = ('full_name', 'date_of_birth', 'department',)
    list_display  = ('full_name', 'date_of_birth', 'department',)