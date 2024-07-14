from django.urls import path

from . import views

urlpatterns = [
    # url for report generation.
    path('', views.report, name='report'),
    path('generate/', views.generate_csv_email, name='generate_csv_email'),
]