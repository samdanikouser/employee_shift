from employee.models import Employee
from location.models import Locations
from schedule_shift.models import EmployeeShift
from django.forms import ModelForm
from django import forms


class EmployeeShiftForm(ModelForm):
    employee_details = forms.ModelChoiceField(queryset=Employee.objects.all(),
                                      widget=forms.Select(attrs={'class': "form-control", 'name': "Name"}))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(),
                                      widget=forms.Select(attrs={'class': "form-control", 'name': "location"}))

    date = forms.DateField(widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift date',
        'type': 'text',
        'name': "date",
        'onfocus': "(this.type = 'date')"
    }))
    from_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift from time',
        'type': 'text',
        'onfocus': "(this.type = 'time')"
    }))
    to_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift to time',
        'type': 'text',
        'onfocus': "(this.type = 'time')"
    }))

    class Meta:
        # write the name of models for which the form is made
        model = EmployeeShift

        # Custom fields
        fields = ["employee_details", "location", "date", "from_time", "to_time"]

    def clean(self):
        # data from the form is fetched using super function
        super(EmployeeShiftForm, self).clean()
        # return any errors if found
        return self.cleaned_data


class DateRangeForm(forms.Form):
    from_date = forms.DateField(label='From Date',widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the from date',
        'type': 'text',
        'name': "from_date",
        'onfocus': "(this.type = 'date')"
    }))
    to_date = forms.DateField(label='To Date', widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the to date',
        'type': 'text',
        'name': "to_date",
        'onfocus': "(this.type = 'date')"
    }))


class AddScheduleForm(forms.Form):
    from_date = forms.DateField(label='From Date',widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the from date',
        'type': 'text',
        'name': "from_date",
        'onfocus': "(this.type = 'date')"
    }))
    to_date = forms.DateField(label='To Date', widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the to date',
        'type': 'text',
        'name': "to_date",
        'onfocus': "(this.type = 'date')"
    }))
    from_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift from time',
        'type': 'text',
        'onfocus': "(this.type = 'time')"
    }))
    to_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift to time',
        'type': 'text',
        'onfocus': "(this.type = 'time')"
    }))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(),
                                      widget=forms.Select(attrs={'class': "form-control", 'name': "location"}))

