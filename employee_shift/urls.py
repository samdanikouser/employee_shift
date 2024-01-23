"""
URL configuration for employee_shift project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from login import views as login_view
from report import views as report_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view.login, name='login'),
    path('signup/', login_view.register, name='signup'),
    path('logout/', login_view.logout_view, name='logout'),
    path('facelogin/', login_view.login_by_face,name='login_by_face'),
    path('dashboard/', login_view.dashboard, name='dashboard'),
    path("employee/", include("employee.urls")),
    path("location/", include("location.urls")),
    path("department/", include("department.urls")),
    path("schedule/", include("schedule.urls")),
    path("report/", report_view.generate_report, name="generate_report"),
    path("email/", report_view.email, name="email"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



