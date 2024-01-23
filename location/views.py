from django.shortcuts import render, redirect, HttpResponse
from location.models import Location
from location.forms import LocationForm


# Create your views here.

def location_list(request):
    location = Location.objects.all()
    return render(request, "location/list.html", {'location': location})


# add employee function
def add_location(request):
    if request.method == "POST":
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.save()
            return redirect("/location/list/")
        else:
            return render(request, "location/add.html",
                          {"form": form})
    return render(request, "location/add.html", {"form": LocationForm()})


# employee delete function
def delete_location(request, id):
    # listings/views.py
    location = Location.objects.get(pk=id)
    if request.method == "POST":
        location.delete()
        return redirect("/location/list/")
    return render(request,
                  'location/delete.html',
                  {'location': location})


# update employee
def update_location(request, id):
    location = Location.objects.get(pk=id)
    if request.method == "POST":
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect("/location/list/")
        else:
            return render(request, "location/update.html",
                          {"location": location, "form": form})
    return render(request, "location/update.html", {"location": location, "form": LocationForm(instance=location)})
