from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    # url for location add,list,delete and update
    path('list/', views.location_list, name='locationList'),
    path('add/', views.add_location, name='addLocation'),
    path('delete/<int:id>', views.delete_location, name='deleteLocation'),
    path('update/<int:id>', views.update_location, name='updateLocation'),
]