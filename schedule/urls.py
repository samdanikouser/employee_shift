from django.urls import path

from . import views

urlpatterns = [
    path('list/', views.schedule_list, name='schedulelist'),
    path('add/', views.add_schedule, name='addschedule'),
    path('delete/<int:id>', views.delete_schedule, name='deleteeschedule'),
    path('update/<int:id>', views.update_schedule, name='updateschedule'),

]