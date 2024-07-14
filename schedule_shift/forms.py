from datetime import timedelta

from employee.models import Employee
from location.models import Locations
from schedule_shift.models import EmployeeShift
from django.forms import ModelForm
from django import forms


class EmployeeShiftForm(ModelForm):
    """Update form"""
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
        # name of models for which the form is made
        model = EmployeeShift

        # Custom fields
        fields = ["employee_details", "location", "date", "from_time", "to_time"]

    def clean(self):
        # data from the form is fetched using super function
        super(EmployeeShiftForm, self).clean()
        # return any errors if found
        return self.cleaned_data


class DateRangeForm(forms.Form):
    """Report date filer form"""
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
    """Add shift form"""
    from_date = forms.DateField(label='From Date',widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'type': 'date',
        'name': "from_date",
        'onfocus': "(this.type = 'date')"
    }))
    to_date = forms.DateField(label='To Date', widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the to date',
        'type': 'date',
        'name': "to_date",
        'onfocus': "(this.type = 'date')"
    }))
    from_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift from time',
        'type': 'time',
        'onfocus': "(this.type = 'time')"
    }))
    to_time = forms.TimeField(widget=forms.TimeInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the shift to time',
        'type': 'time',
        'onfocus': "(this.type = 'time')"
    }))
    location = forms.ModelChoiceField(queryset=Locations.objects.all(),
                                      widget=forms.Select(attrs={'class': "form-control", 'name': "location"}))
    employee_details = forms.ModelMultipleChoiceField(queryset=Employee.objects.all(), widget=forms.CheckboxSelectMultiple)


    def clean(self):
        cleaned_data = super().clean()
        employee_details = cleaned_data.get('employee_details')
        to_date = cleaned_data.get('to_date')
        from_date = cleaned_data.get('from_date')
        date = from_date
        if from_date <= date.today():
            self._errors['from_date'] = self.error_class([
                'Please select future date.'])
        if employee_details and date:
            while date <= to_date:
                for employee_id in employee_details:
                    # Check if there's any existing shift for the same employee at the same time
                    existing_shifts = EmployeeShift.objects.filter(
                        employee_details=employee_id,
                        date=date,
                    )
                    if existing_shifts.exists():
                        self._errors['employee_details'] = self.error_class([
                            str(employee_id)+'is already scheduled for this date.'+str(date)])
                date += timedelta(days=1)

        return cleaned_data

