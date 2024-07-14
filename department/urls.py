from django.urls import path
from django.views.generic import TemplateView

from . import views
urlpatterns = [
    # url for departments add,list,delete and update
    path('list/', views.department_list, name='departmentList'),
    path('add/', views.add_department, name='addDepartment'),
    path('delete/<int:id>', views.delete_department, name='deleteDepartment'),
    path('update/<int:id>', views.update_department, name='updateDepartment'),
]