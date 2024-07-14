from django.urls import path
from . import views

urlpatterns = [
    # url for employee add,list,delete and update
    path('list/', views.employee_list, name='employeeList'),
    path('add/', views.add_employee, name='addEmployee'),
    path('delete/<int:emp_id>', views.delete_emp, name='deleteEmployee'),
    path('update/<int:emp_id>', views.update_emp, name='updateEmployee')
]