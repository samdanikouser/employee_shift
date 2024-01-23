import datetime

from department.models import Department
from employee.models import Employee
from django.forms import ModelForm
from django import forms


# define the class of a form
class EmployeeForm(ModelForm):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                                error_messages={'required': "Please Enter your Name "})
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        widget=forms.Select(attrs={'class': "form-control", 'name': "department"}))
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the date of birth',
        'type': 'text',
        'name': "data_of_birth",
        'onfocus': "(this.type = 'date')"
    }))

    class Meta:
        # write the name of models for which the form is made
        model = Employee

        # Custom fields
        fields = ["full_name", "date_of_birth", "department"]

    def clean(self):
        # data from the form is fetched using super function
        super(EmployeeForm, self).clean()

        year = datetime.datetime.today().year

        # extract the username and text field from the data
        full_name = self.cleaned_data.get('full_name')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        age_based_on_year = int(year) - int(date_of_birth.year)

        # conditions to be met for the username length
        if age_based_on_year <= 20:
            self._errors['date_of_birth'] = self.error_class([
                'The selected date is not valid'])
        if len(full_name) < 5:
            self._errors['full_name'] = self.error_class([
                'Minimum 5 characters required'])
        # return any errors if found
        return self.cleaned_data