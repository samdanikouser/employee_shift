from department.models import Department
from employee.models import Employee
from django.forms import ModelForm
from django import forms
import datetime


class EmployeeForm(ModelForm):
    """Form that is used for Create,update of employee
        which is passed to template file where we need not code
         in html file explicitly as we can validate the data
          if required using form and show errors if any"""
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
        """specifies the model on which the form operate and the list of fields"""
        model = Employee
        fields = ["full_name", "date_of_birth", "department"]

    def clean(self):
        """ used to perform validation that requires access to
        multiple fields of a form or a model instance,
        where employee age should be more than 20 and must have name with at least 5 char"""
        super(EmployeeForm, self).clean()

        year = datetime.datetime.today().year

        full_name = self.cleaned_data.get('full_name')
        date_of_birth = self.cleaned_data.get('date_of_birth')
        age_based_on_year = int(year) - int(date_of_birth.year)

        if age_based_on_year <= 20:
            self._errors['date_of_birth'] = self.error_class([
                'The selected date is not valid, the age should be min of 20'])
        if len(full_name) < 5:
            self._errors['full_name'] = self.error_class([
                'Minimum 5 characters required'])
        return self.cleaned_data
