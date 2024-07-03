from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .forms import UserRegistrationForm
from .models import UserProfile


def user_login(request):
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
    logout(request)
    return redirect('login')


def register(request):
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
    return render(request, 'home.html', {'user': request.user})


@login_required
def settings(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
            'user_profile': user_profile
        }
    return render(request, 'settings.html',context)