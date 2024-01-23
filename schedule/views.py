from datetime import datetime
import pandas as pd
from django.shortcuts import render, redirect
from employee.models import Employee
from location.models import Location
from schedule.forms import ScheduleForm
from schedule.models import Scheduler
import django_filters


def schedule_list(request):
    show_table = False
    if request.method == "POST":
        show_table = True
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        scheduler = Scheduler.objects.filter(date__range=[from_date, to_date])
        return render(request, "schedules/list.html", {'scheduler': scheduler, 'show_table': show_table})
    return render(request, "schedules/list.html", {"show_table": show_table})


def add_schedule(request):
    employees_scheduler = Employee.objects.all()
    location = Location.objects.all()
    if request.method == "POST":
        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")
        from_time = request.POST.get("from_time")
        to_time = request.POST.get("to_time")
        location = request.POST.get("location")
        employee_list = request.POST.getlist("checks")
        # difference between each date. D means one day
        D = 'D'
        date_list = pd.date_range(from_date, to_date, freq=D)
        for date in date_list:
            for employee_id in employee_list:
                scheduler = Scheduler()
                scheduler.location = Location.objects.get(name=location)
                scheduler.date = date
                scheduler.from_time = from_time
                scheduler.to_time = to_time
                scheduler.employee = Employee.objects.get(employee_id=employee_id)
                scheduler.save()
        return redirect("/schedule/add/")
    return render(request, "schedules/add.html",
                  {'employees_scheduler': employees_scheduler, 'location': location})


# employee delete function
def delete_schedule(request, id):
    # listings/views.py
    scheduler = Scheduler.objects.get(pk=id)
    if request.method == "POST":
        scheduler.delete()
        return redirect("/schedule/list/")
    return render(request,
                  'schedules/delete.html',
                  {'scheduler': scheduler})


# update employee
def update_schedule(request, id):
    scheduler = Scheduler.objects.get(pk=id)
    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=scheduler)
        if form.is_valid():
            form.save()
            return redirect("/schedule/list/")
        else:
            return render(request, "schedules/update.html",
                          {"scheduler": scheduler, "form": form})
    return render(request, "schedules/update.html", {"scheduler": scheduler, "form": ScheduleForm(instance=scheduler)})
