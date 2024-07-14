from django.urls import path
from . import views

urlpatterns = [
    # url for home,login,logout,profile and registration
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
