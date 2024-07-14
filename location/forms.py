from location.models import Locations
from django.forms import ModelForm
from django import forms


class LocationForm(ModelForm):
    """Form that is used for Create,update of location
            which is passed to template file where we need not code
             in html file explicitly as we can validate the data
              if required using form and show errors if any"""
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter Location Name"})

    class Meta:
        """specifies the model on which the form operate and the list of fields"""
        model = Locations
        fields = ["name"]

    def clean(self):
        """perform validation so that location name should not be less than 5 char
        and name must be unique"""
        super(LocationForm, self).clean()

        name = self.cleaned_data.get('name')
        if Locations.objects.filter(name=name).exists():
            self._errors['name'] = self.error_class([
                'Name already exists'])
        if len(name) < 5:
            self._errors['name'] = self.error_class([
                'Minimum 5 characters required'])
        return self.cleaned_data

