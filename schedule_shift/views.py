from datetime import datetime
from datetime import timedelta


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .filters import EmployeeShiftFilter
from employee.models import Employee
from location.models import Locations
from schedule_shift.forms import EmployeeShiftForm, DateRangeForm
from schedule_shift.models import EmployeeShift
from django.core.paginator import Paginator


@login_required
def schedule_list(request):
    show_table = False
    page_obj = None
    from_date = None
    to_date = None
    if request.method == "POST" or "filter" in request.GET or (request.GET and "page" in request.GET):
        show_table = True
        form = DateRangeForm()
        if request.method == "POST":
            form = DateRangeForm(request.POST)
        else:
            form = DateRangeForm(request.GET)

        if form.is_valid():
            print("sample")
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            if "employee_details__full_name" in request.GET and request.GET['employee_details__full_name']:
                scheduler = EmployeeShift.objects.filter(employee_details__full_name=request.GET.get("employee_details__full_name"))
            elif "location__name" in request.GET and request.GET['location__name']:
                scheduler = EmployeeShift.objects.filter(location__name = request.GET.get("location__name"))
            elif "location__name" in request.GET and request.GET['location__name'] and "employee_details__full_name" in request.GET  and request.GET['employee_details__full_name']:
                scheduler = EmployeeShift.objects.filter(employee_details__full_name=request.GET.get("employee_details__full_name"),location__name = request.GET.get("location__name"))
            else:
                scheduler = EmployeeShift.objects.filter(date__range=[from_date, to_date])

            # Apply filters
            item_filter = EmployeeShiftFilter(request.GET, queryset=scheduler)
            items = item_filter.qs

            # Pagination
            paginator = Paginator(items, 10)  # Show 10 items per page
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, "schedule_shift/list.html", {'items': page_obj, 'show_table': show_table, 'item_filter': item_filter,"form":form, 'from_date': from_date, 'to_date': to_date})
    return render(request, "schedule_shift/list.html", {"show_table": show_table,"form":DateRangeForm(), 'from_date': from_date, 'to_date': to_date})


@login_required
def add_schedule(request):
    employees_scheduler = Employee.objects.all()
    from_date = None
    to_date = None
    from_time = None
    to_time = None
    location =None

    if request.method == "GET":
        from_date = request.GET.get("from_date")
        to_date = request.GET.get("to_date")
        from_time = request.GET.get("from_time")
        to_time = request.GET.get("to_time")
        location = request.GET.get("location")
    print(request.GET)
    # Pagination
    paginator = Paginator(employees_scheduler, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    location = Locations.objects.all()
    if request.method == "POST":
        from_date = datetime.strptime(request.POST.get("from_date"), '%Y-%m-%d')
        to_date = datetime.strptime(request.POST.get("to_date"), '%Y-%m-%d')
        from_time = request.POST.get("from_time")
        to_time = request.POST.get("to_time")
        location = request.POST.get("location")
        employee_list = request.POST.getlist("checks")
        date = from_date
        while date <= to_date:
            for employee_id in employee_list:
                EmployeeShift.objects.create(date=date,from_time=from_time,to_time = to_time,
                                             location=Locations.objects.get(name=location),
                                             employee_details = Employee.objects.get(employee_id=employee_id),
                                             )
            date += timedelta(days=1)
        messages.success(request, f'Scheduled Successfully!')
        return redirect("/shiftSchedule/add/")
    return render(request, "schedule_shift/add.html",
                  {'employees_scheduler': page_obj, 'location': location,'from_date':from_date,
                   "to_date":to_date,"from_time":from_time,"to_time":to_time})


# schedule delete function
@login_required
def delete_schedule(request, id):
    # listings/views.py
    scheduler = EmployeeShift.objects.get(pk=id)
    if request.method == "POST":
        scheduler.delete()
        return redirect("/shiftSchedule/list/")
    return render(request,
                  'schedule_shift/delete.html',
                  {'scheduler': scheduler})


# update schedule
@login_required
def update_schedule(request, id):
    scheduler = EmployeeShift.objects.get(pk=id)
    if request.method == "POST":
        form = EmployeeShiftForm(request.POST, instance=scheduler)
        if form.is_valid():
            form.save()
            return redirect("/shiftSchedule/list/")
        else:
            return render(request, "schedule_shift/update.html",
                          {"scheduler": scheduler, "form": form})
    return render(request, "schedule_shift/update.html", {"scheduler": scheduler, "form": EmployeeShiftForm(instance=scheduler)})
