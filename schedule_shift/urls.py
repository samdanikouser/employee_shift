from django.urls import path

from . import views

urlpatterns = [
    # url for shift scheduling add,delete,update and list
    path('list/', views.schedule_list, name='scheduleList'),
    path('add/', views.add_schedule, name='addSchedule'),
    path('delete/<int:id>', views.delete_schedule, name='deleteeSchedule'),
    path('update/<int:id>', views.update_schedule, name='updateSchedule'),

]
