import csv

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import EmailMessage
from django.contrib import messages
from schedule_shift.models import EmployeeShift


@login_required
def report(request):
    return render(request, "report/report.html")


@login_required
def generate_csv_email(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date', '')
        end_date = request.POST.get('end_date', '')
        action = request.POST.get('action', '')

        queryset = EmployeeShift.objects.filter(
            date__range=[start_date, end_date])

        if action == 'generate_csv':
            # Generate CSV file
            csv_filename = f"shiftSchedule_data_of_data_{start_date}_to_{end_date}.csv"
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{csv_filename}"'

            writer = csv.writer(response)

            writer.writerow(["Employee Id", "Name", "Department", "Location", "From Date", "From Time", "To Time"])
            for schedule_id in queryset:
                report_schedule_list = EmployeeShift.objects.get(pk=schedule_id.id)
                print(report_schedule_list)
                writer.writerow([report_schedule_list.id, report_schedule_list.employee_details.full_name,
                                 report_schedule_list.employee_details.department.name,
                                 report_schedule_list.location.name, report_schedule_list.date,
                                 report_schedule_list.from_time, report_schedule_list.to_time])

            return response

        elif action == 'send_email':
            email_address = request.POST.get('email')
            # Generate CSV file in memory
            csv_data = []
            csv_data.append(["Employee Id", "Name", "Department", "Location", "From Date", "From Time", "To Time"])  # Replace with your actual model fields

            for schedule_id in queryset:
                report_schedule_list = EmployeeShift.objects.get(pk=schedule_id.id)
                csv_data.append([report_schedule_list.id, report_schedule_list.employee_details.full_name,
                                     report_schedule_list.employee_details.department.name,
                                     report_schedule_list.location.name, report_schedule_list.date,
                                     report_schedule_list.from_time, report_schedule_list.to_time])

            # Prepare email with CSV attachment
            csv_filename = f"shiftSchedule_data_of_data_{start_date}_to_{end_date}.csv"
            email_subject = f"Data from {start_date} to {end_date}"
            email_body = "Attached is the CSV file with data of shift schedule."

            email = EmailMessage(email_subject, email_body, to=[email_address])
            email.attach(csv_filename, '\n'.join(','.join(map(str, row)) for row in csv_data), 'text/csv')
            email.send()
            messages.success(request, f'Email send Successfully!')
            return render(request, 'report/report.html')

    return render(request, 'report/report.html')
