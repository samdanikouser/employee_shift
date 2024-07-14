from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from login_reg.models import UserProfile


class UserRegistrationForm(UserCreationForm):
    """User registration form for adding a new user"""
    class Meta:
        """specifies the model on which the form operate and the list of fields"""
        model = User
        fields = ['username', 'password1', 'password2']


class UserForm(forms.ModelForm):
    """User form for profile details"""
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "first_name"}),
                                error_messages={'required': "Please Enter your First Name "})
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "last_name"}),
                                 error_messages={'required': "Please Enter your Last Name "})
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "email"}),
                                 error_messages={'required': "Please Enter your email "})

    class Meta:
        """specifies the model on which the form operate and the list of fields"""
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    """Profile form for profile details"""
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "location"}),
                               error_messages={'required': "Please Enter your Location "})

    location = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", 'name': "location"}),
                                error_messages={'required': "Please Enter your Location "})
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        'class': "form-control text-center fw-bold",
        'style': 'max-width: auto;',
        'placeholder': 'Please enter the date of birth',
        'type': 'text',
        'name': "birth_date",
        'onfocus': "(this.type = 'date')"
    }))

    class Meta:
        """specifies the model on which the form operate and the list of fields"""
        model = UserProfile
        fields = ('bio', 'location', 'birth_date', 'profile_pic')

    def __init__(self, *args, **kwargs):
        """For showing profile picture"""
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control-file'})
