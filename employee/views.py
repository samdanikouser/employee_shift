from django.contrib.auth.decorators import login_required
from department.models import Department
from employee.forms import EmployeeForm
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .filters import EmployeeFilter
from .models import Employee


@login_required
def employee_list(request):
    """To display all the employee details"""
    emps = Employee.objects.all()

    # Apply filters
    item_filter = EmployeeFilter(request.GET, queryset=emps)
    items = item_filter.qs
    # Apply filters
    item_filter = EmployeeFilter(request.GET, queryset=emps)
    items = item_filter.qs

    # Pagination
    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,
        'item_filter': item_filter,
    }

    return render(request, "employee/list.html", context)


# add employee function
@login_required
def add_employee(request):
    """For adding the employee details, where data is passed to the
     function from the form and then validated and if valid stored in DB"""
    department = Department.objects.all()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect("/employee/list/")
        else:
            return render(request, "employee/add.html",
                          {"form": form})
    return render(request, "employee/add.html", {'department': department, "form": EmployeeForm()})


# employee delete function
@login_required
def delete_emp(request, emp_id):
    """Delete employee data based on ID """
    emp = Employee.objects.get(pk=emp_id)
    if request.method == "POST":
        emp.delete()
        return redirect("/employee/list/")
    return render(request,
                  'employee/delete.html',
                  {'emp': emp})


# update employee
@login_required
def update_emp(request, emp_id):
    """Update employee data based on ID and redirect to list view if not to the update page """
    emp = Employee.objects.get(pk=emp_id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect("/employee/list/")
        else:
            return render(request, "employee/update.html",
                          {"emp": emp, "form": form})
    return render(request, "employee/update.html", {"emp": emp, "form": EmployeeForm(instance=emp)})
