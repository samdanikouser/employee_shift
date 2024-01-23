from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('list/', views.employee_list, name='employeelist'),
    path('add/', views.add_employee, name='addemployee'),
    path('delete/<int:emp_id>', views.delete_emp, name='deleteemployee'),
    path('update/<int:emp_id>', views.update_emp, name='updateemployee'),
    path('profile/', views.profile, name='profile'),
    path("checkin/<int:emp_id>", views.checkin_emp, name="checkin"),
    path("enroll/<int:emp_id>", views.enroll_emp, name="enroll"),
]