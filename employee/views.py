from django.template.loader import render_to_string

from employee.forms import EmployeeForm
from django.shortcuts import render, redirect
from .models import Employee, Department, Enrollment
from django.http import JsonResponse
import cv2
import uuid
import shutil
import os
import face_recognition
import pickle
from django.views.decorators.csrf import csrf_exempt
from test import test

PATH = "assets"


# Create your views here.

def employee_list(request):
    emps = Employee.objects.all()
    return render(request, "employee/list.html", {'emps': emps})


# add employee function
def add_employee(request):
    department = Department.objects.all()
    if request.method == "POST":
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save(commit=False)
            employee.save()
            return redirect("/employee/list/")
        else:
            return render(request, "employee/add.html",
                          {"form": form})
    return render(request, "employee/add.html", {'department': department, "form": EmployeeForm()})


# employee delete function
def delete_emp(request, emp_id):
    # listings/views.py
    emp = Employee.objects.get(pk=emp_id)
    if request.method == "POST":
        emp.delete()
        return redirect("/employee/list/")
    return render(request,
                  'employee/delete.html',
                  {'emp': emp})


# update employee
def update_emp(request, emp_id):
    emp = Employee.objects.get(pk=emp_id)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=emp)
        if form.is_valid():
            form.save()
            return redirect("/employee/list/")
        else:
            return render(request, "employee/update.html",
                          {"emp": emp, "form": form})
    return render(request, "employee/update.html", {"emp": emp, "form": EmployeeForm(instance=emp)})


def profile(request):
    emp = Employee.objects.get(full_name=request.user.username)
    return render(request, "employee/profile.html", {"emp":emp})


@csrf_exempt
def checkin_emp(request, emp_id):
    if request.method == "POST":
        file = request.FILES['image']
        file.filename = f"{uuid.uuid4()}.png"

        # example of how you can save the file
        with open(file.filename, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        if not os.path.exists(PATH):
            os.makedirs(PATH)
        login = False
        label, image_name = test(image=file,
                                 model_dir='/Users/samdanikouser/Desktop/login/employee_shift/resources/anti_spoof_models',
                                 device_id=0)
        if label == 1:
            user_name, match_status = recognize(cv2.imread(file.filename), emp_id, login)

            # if found a match, set attendance log here
            if match_status:
                pass

            os.remove(file.filename)
            employee = Employee.objects.get(pk=emp_id)
            return JsonResponse({'status': 200, 'user': user_name, 'match_status': match_status, "emp_id": emp_id,
                                 "employee": employee.full_name})
        else:
            os.remove(file.filename)
            return JsonResponse({'error': 'Face is not real', 'status': 400, 'code': 1000})
    return render(request, "employee/checkin.html", {"emp_id": emp_id})


@csrf_exempt
def enroll_emp(request, emp_id):
    if request.method == "POST":
        file = request.FILES['image']
        file.filename = str(emp_id) + ".png"
        text = str(emp_id)

        # example of how you can save the file
        with open(file.filename, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)

        if not os.path.exists(PATH):
            os.makedirs(PATH)

        shutil.copy(file.filename, os.path.join(PATH, '{}.png'.format(text)))
        label, image_name = test(image=file,
                                 model_dir='/Users/samdanikouser/Desktop/login/employee_shift/resources/anti_spoof_models',
                                 device_id=0)
        if label == 1:
            image = face_recognition.load_image_file(file.filename)
            face_locations = face_recognition.face_locations(image)

            print(f"face_locations: {face_locations}")
            if not face_locations:
                os.remove(file.filename)
                return JsonResponse({'error': 'Faces not detected.Please try again', 'status': 400, 'code': 1000})
            login = True
            user_name, match_status = recognize(cv2.imread(file.filename), emp_id, login)
            if match_status:
                if int(user_name) == int(emp_id):
                    pass
                os.remove(file.filename)
                return JsonResponse({'error': 'Your already Enrolled as other employee', 'status': 400, 'code': 1000})

            embeddings = face_recognition.face_encodings(cv2.imread(file.filename))

            file_ = open(os.path.join(PATH, '{}.pickle'.format(text)), 'wb')
            pickle.dump(embeddings, file_)
            print(file.filename)

            os.remove(file.filename)
            Employee_id_enroll_status = Employee.objects.get(pk=emp_id)
            Enroll = Enrollment()
            Enroll.employee = Employee_id_enroll_status
            Enroll.photo = str(emp_id) + ".pickle"
            Enroll.save()

            Employee_id_enroll_status.enrollment_status = True
            Employee_id_enroll_status.save()

            return JsonResponse({'status': 200})
        else:
            os.remove(file.filename)
            return JsonResponse({'error': 'Faces not real', 'status': 400, 'code': 1000})
    return render(request, "employee/enroll.html", {"emp_id": emp_id})


def recognize(img, emp_id, login):
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
    if not login:
        Enrolled_image = Enrollment.objects.get(employee=Employee.objects.get(pk=emp_id))
        while (not match) and (j < len(db_dir)):
            if db_dir[j] == str(Enrolled_image.photo):
                path_ = os.path.join(PATH, str(Enrolled_image.photo))

                file = open(path_, 'rb')
                embeddings = pickle.load(file)[0]

                match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]
            j += 1
        if match:
            return db_dir[j - 1][:-7], True
        else:
            return 'unknown_person', False
    else:
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
