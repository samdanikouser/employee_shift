from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserRegistrationForm, UserForm, ProfileForm
from .models import UserProfile


def user_login(request):
    """Function for user login,check for password and username and
        returns to home is details are correct"""
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                login(request, user)
                return redirect('home')
            else:
                error_message = 'Invalid password'
        except User.DoesNotExist:
            error_message = 'User does not exist'
    else:
        error_message = None
    return render(request, 'login.html', {'error_message': error_message})


def user_logout(request):
    """Function for Logout ,which will redirect to login page"""
    logout(request)
    return redirect('login')


def register(request):
    """Function for user registration, account is created"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration.html', {'form': form})


@login_required
def home(request):
    """Function that will be redirected on login success """
    return render(request, 'home.html', {'user': request.user})


@login_required
def settings(request):
    """Function to show user details"""
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
            'user_profile': user_profile
        }
    return render(request, 'settings.html',context)


@login_required
def edit_profile(request):
    """Function to edit user details"""
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('settings')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})
