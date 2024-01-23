from django.shortcuts import render, redirect, HttpResponse
from department.models import Department
from department.forms import DepartmentForm


# Create your views here.

def department_list(request):
    department = Department.objects.all()
    return render(request, "department/list.html", {'department': department})


# add employee function
def add_department(request):
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


# employee delete function
def delete_department(request, id):
    # listings/views.py
    department = Department.objects.get(pk=id)
    if request.method == "POST":
        department.delete()
        return redirect("/department/list/")
    return render(request,
                  'department/delete.html',
                  {'department': department})


# update employee
def update_department(request, id):
    department = Department.objects.get(pk=id)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect("/department/list/")
        else:
            return render(request, "department/update.html",
                          {"department": department, "form": form})
    return render(request, "department/update.html", {"department": department, "form": DepartmentForm(instance=department)})
