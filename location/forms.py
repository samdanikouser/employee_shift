from location.models import Locations
from django.forms import ModelForm
from django import forms


class LocationForm(ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "name"}),
                           error_messages={'required': "Please Enter Location Name"})

    class Meta:
        model = Locations

        fields = ["name"]

    def clean(self):
        super(LocationForm, self).clean()

        name = self.cleaned_data.get('name')
        if len(name) < 5:
            self._errors['name'] = self.error_class([
                'Minimum 5 characters required'])
        return self.cleaned_data

