from department.models import Department
from django.forms import ModelForm
from django import forms


class DepartmentForm(ModelForm):
    """Form that is used for Create,update of department
    which is passed to template file where we need not code
     in html file explicitly as we can validate the data
      if required using form and show errors if any"""
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter Department Name"})

    class Meta:
        """specifies the model on which the form operate and the list of fields"""
        model = Department
        fields = ["name"]

    def clean(self):
        """ used to perform validation that requires access to multiple fields of a form or a model instance"""
        super(DepartmentForm, self).clean()

        name = self.cleaned_data.get('name')
        if len(name) < 5:
            self._errors['name'] = self.error_class([
                'Minimum 5 characters required'])
        return self.cleaned_data

