from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from department.filters import DepartmentFilter
from department.forms import DepartmentForm
from department.models import Department
from django.core.paginator import Paginator


# list employee Department function
@login_required
def department_list(request):
    """To get all the values from department table and view"""
    department = Department.objects.all()

    """Apply filters"""
    item_filter = DepartmentFilter(request.GET, queryset=department)
    items = item_filter.qs

    """Pagination"""
    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    """ data to pass to template file"""
    context = {
        'items': page_obj,
        'item_filter': item_filter,
    }

    return render(request, "department/list.html", context)


# add employee Department function
@login_required
def add_department(request):
    """ get the form data from department form.py and
    check for if its valid and then stores the department data in to the table"""
    if request.method == "POST":
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save(commit=False)
            department.save()
            return redirect("/department/list/")
        else:
            return render(request, "department/add.html",
                          {"form": form})
    return render(request, "department/add.html", {"form": DepartmentForm()})


# employee delete Department function
@login_required
def delete_department(request, id):
    """This function is used to delete the department based on the ID of the
     department stores in table, on delete successfully redirecting to list page"""
    department = Department.objects.get(pk=id)
    if request.method == "POST":
        department.delete()
        return redirect("/department/list/")
    return render(request,
                  'department/delete.html',
                  {'department': department})


# update employee Department
@login_required
def update_department(request, id):
    """This function is used to update the department
    based on the ID of the department stores in table
    and returns to list pade on successfully
    updated else to update template"""
    department = Department.objects.get(pk=id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect("/department/list/")
        else:
            return render(request, "department/update.html",
                          {"department": department, "form": form})
    return render(request, "department/update.html",
                  {"department": department, "form": DepartmentForm(instance=department)})
