from location.models import Location
from employee.models import Employee
from django.forms import ModelForm
from django import forms

from schedule.models import Scheduler


# define the class of a form
class ScheduleForm(ModelForm):
    employee = forms.ModelChoiceField(queryset=Employee.objects.all(),
                                        widget=forms.Select(attrs={'class': "form-control", 'name': "employee"}))
    location = forms.ModelChoiceField(queryset=Location.objects.all(),
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
        model = Scheduler

        # Custom fields
        fields = ["employee", "location", "date","from_time","to_time"]

    def clean(self):
        # data from the form is fetched using super function
        super(ScheduleForm, self).clean()
        # return any errors if found
        return self.cleaned_data
