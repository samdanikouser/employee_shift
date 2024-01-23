import csv
from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.mail import EmailMessage
from schedule.models import Scheduler

def generate_report(request):
    only_mail = False
    if request.method == "POST":
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')
        if "report_generate" in request.POST:
            schedule_date_list = Scheduler.objects.filter(date__range=[from_date, to_date])
            today = date.today()
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="Employee_schedule"' + str(today) + '.csv'},
            )
            writer = csv.writer(response)
            writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "From Time", "To Time"])
            for schedule_id in schedule_date_list:
                report_schedule_list = Scheduler.objects.get(pk=schedule_id.id)
                writer.writerow([report_schedule_list.id, report_schedule_list.employee.full_name,
                                 report_schedule_list.employee.department.name,
                                 report_schedule_list.location.name, report_schedule_list.date,
                                 report_schedule_list.from_time,report_schedule_list.to_time])
            return response
        if "email_popup" in request.POST:
            return render(request, "report/add_email.html", {"from_date": from_date, "to_date": to_date,"only_mail":only_mail})
        if "send_email" in request.POST:
            schedule_date_list = Scheduler.objects.filter(date__range=[from_date, to_date])
            recip_email = request.POST.get("email")
            today = date.today()
            response = HttpResponse(
                content_type="text/csv",
                headers={"Content-Disposition": 'attachment; filename="Employee_schedule"' + str(today) + '.csv'},
            )
            writer = csv.writer(response)
            writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "From Time", "To Time"])
            for schedule_id in schedule_date_list:
                report_schedule_list = Scheduler.objects.get(pk=schedule_id.id)
                writer.writerow([report_schedule_list.id, report_schedule_list.employee.full_name,
                                 report_schedule_list.employee.department.name,
                                 report_schedule_list.location.name, report_schedule_list.date,
                                 report_schedule_list.from_time, report_schedule_list.to_time])
            subject = 'Employees Schedule Report'
            message = 'Report for Employee Schedule for the mentioned date in Report.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [recip_email, ]
            mail = EmailMessage(subject, message, email_from, recipient_list)
            mail.attach('employee_schedule.csv', response.getvalue(), 'text/csv')
            mail.send()
    return render(request, "report/report.html", {})


def email(request):
    only_mail = True
    if request.method == "POST":
        from_date = request.POST.get('from_dates')
        to_date = request.POST.get('to_dates')
        schedule_date_list = Scheduler.objects.filter(date__range=[from_date, to_date])
        recip_email = request.POST.get("email")
        today = date.today()
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="Employee_schedule"' + str(today) + '.csv'},
        )
        writer = csv.writer(response)
        writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "From Time", "To Time"])
        for schedule_id in schedule_date_list:
            report_schedule_list = Scheduler.objects.get(pk=schedule_id.id)
            writer.writerow([report_schedule_list.id, report_schedule_list.employee.full_name,
                             report_schedule_list.employee.department.name,
                             report_schedule_list.location.name, report_schedule_list.date,
                             report_schedule_list.from_time, report_schedule_list.to_time])
        subject = 'Employees Schedule Report'
        message = 'Report for Employee Schedule for the mentioned date in Report.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [recip_email, ]
        mail = EmailMessage(subject, message, email_from, recipient_list)
        mail.attach('employee_schedule.csv', response.getvalue(), 'text/csv')
        mail.send()
    return render(request, "report/add_email.html", {"only_mail":only_mail})


# send auto mail
def cron_job_function(request):
    if "send_email" in request.POST:
        today = date.today()
        schedule_date_list = Scheduler.objects.filter(from_date=today)
        recip_email = request.POST.get("email")
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="Employee_schedule"' + str(today) + '.csv'},
        )
        writer = csv.writer(response)
        writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "To Date"])
        for schedule_id in schedule_date_list:
            report_schedule_list = Scheduler.objects.get(pk=schedule_id.id)
            writer.writerow([report_schedule_list.id, report_schedule_list.employee.full_name,
                             report_schedule_list.employee.department.department,
                             report_schedule_list.location.location, report_schedule_list.from_date,
                             report_schedule_list.to_Date])
        subject = 'Employees Schedule Report'
        message = 'Report for Employee Schedule for the mentioned date in Report.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [recip_email, ]
        mail = EmailMessage(subject, message, email_from, recipient_list)
        mail.attach('employee_schedule.csv', response.getvalue(), 'text/csv')
        mail.send()

