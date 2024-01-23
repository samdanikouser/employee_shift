import os
import pickle
import uuid

import cv2
import face_recognition
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth

from django.contrib.auth.models import User
from employee.models import Employee
from test import test
from .forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login as facelogin

PATH = 'assets'


# Create your views here.

# registration function
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user_name = form.cleaned_data['username']
            employee = Employee()
            employee.full_name = user_name
            employee.save()
            messages.success(request, 'You are now able to log in')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'login_reg/registration.html', {'form': form, 'title': 'register here'})


# Login function
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            form = auth.login(request, user)
            messages.success(request, f' welcome {username} !!')
            return redirect('/dashboard/')
        else:
            messages.info(request, f'account done not exit plz sign in')
    form = auth.forms.AuthenticationForm()
    return render(request, 'login_reg/login.html', {'form': form, 'title': 'log in'})


# logout function
def logout_view(request):
    auth.logout(request)
    return redirect('login')


def dashboard(request):
    return render(request, 'dashboard.html', {})

def recognize(img):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found', False
    else:
        embeddings_unknown = embeddings_unknown[0]

    match = False
    j = 0

    db_dir = sorted([j for j in os.listdir(PATH) if j.endswith('.pickle')])
    # db_dir = sorted(os.listdir(DB_PATH))
    while ((not match) and (j < len(db_dir))):
        path_ = os.path.join(PATH, db_dir[j])

        file = open(path_, 'rb')
        embeddings = pickle.load(file)[0]

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]

        j += 1

    if match:
        return db_dir[j - 1][:-7], True
    else:
        return 'unknown_person', False


@csrf_exempt
def login_by_face(request):
    if request.method == "POST":
        file = request.FILES['image']
        file.filename = f"{uuid.uuid4()}.png"

        # example of how you can save the file
        with open(file.filename, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        if not os.path.exists(PATH):
            os.makedirs(PATH)

        label, image_name = test(image=file,
                                 model_dir='/Users/samdanikouser/Desktop/login/employee_shift/resources/anti_spoof_models',
                                 device_id=0)
        if label == 1:
            user_name, match_status = recognize(cv2.imread(file.filename))

            # if found a match, set attendance log here
            if match_status:
                employee_detail = Employee.objects.get(employee_id=int(user_name))
                users = User.objects.filter(username=employee_detail.full_name)
                if len(users) > 0:
                    user_exists = User.objects.filter(username=users[0]).exists()
                    if user_exists:
                        user = User.objects.get(username=users[0].username)
                        facelogin(request, user)
                    os.remove(file.filename)
                    return JsonResponse({'status': 200, 'user': user_name, 'match_status': match_status})
            else:
                os.remove(file.filename)
                return JsonResponse({'status': 200, 'user': user_name, 'match_status': False})
        return JsonResponse({'status': 200, 'match_status': False})
    return render(request, "login_reg/facelogin.html", {})

