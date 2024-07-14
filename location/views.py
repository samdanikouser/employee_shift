from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from location.filters import LocationFilter
from location.forms import LocationForm
from location.models import Locations
from django.core.paginator import Paginator


# list employee location function
@login_required
def location_list(request):
    """Function to display all the location """
    location = Locations.objects.all()
    # Apply filters
    item_filter = LocationFilter(request.GET, queryset=location)
    items = item_filter.qs
    # Apply filters
    item_filter = LocationFilter(request.GET, queryset=location)
    items = item_filter.qs

    # Pagination
    paginator = Paginator(items, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'items': page_obj,
        'item_filter': item_filter,
    }

    return render(request, "location/list.html", context)


# add employee loc function
@login_required
def add_location(request):
    """Function to add the location ,on successfully adding redirect to list view else to add template file """
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


# employee loc delete function
@login_required
def delete_location(request, id):
    """Delete location based on ID"""
    location = Locations.objects.get(pk=id)
    if request.method == "POST":
        location.delete()
        return redirect("/location/list/")
    return render(request,
                  'location/delete.html',
                  {'location': location})


# update location
@login_required
def update_location(request, id):
    """Update location based on ID and redirect to list view if not remains in update page """
    location = Locations.objects.get(pk=id)
    if request.method == "POST":
        print(request.POST)
        form = LocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            return redirect("/location/list/")
        else:
            return render(request, "location/update.html",
                          {"location": location, "form": form})
    return render(request, "location/update.html", {"location": location, "form": LocationForm(instance=location)})


