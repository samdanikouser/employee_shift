import csv
from datetime import date
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from schedule_shift.models import EmployeeShift

class Command(BaseCommand):
    help = 'Generates daily report of employee shifts and sends it via email.'

    def handle(self, *args, **kwargs):
        today = date.today()
        filename = f"employee_shifts_{today}.csv"

        # Query employee shifts for the current day
        shifts = EmployeeShift.objects.filter(date=today)

        # Generate CSV content
        csv_data = []
        csv_data.append(["Employee Id", "Name", "Department", "Location", "From Date", "From Time",
                         "To Time"])

        for schedule_id in shifts:
            report_schedule_list = EmployeeShift.objects.get(pk=schedule_id.id)
            csv_data.append([report_schedule_list.id, report_schedule_list.employee_details.full_name,
                             report_schedule_list.employee_details.department.name,
                             report_schedule_list.location.name, report_schedule_list.date,
                             report_schedule_list.from_time, report_schedule_list.to_time])

        # Prepare CSV file
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(csv_data)

        # Prepare email with CSV attachment
        email_subject = f"Employee Shift Report - {today}"
        email_body = "Please find attached the employee shift report for today."

        email = EmailMessage(email_subject, email_body, to=['samdani.shareef6@gmail.com'])
        email.attach_file(filename)
        email.send()

        self.stdout.write(self.style.SUCCESS('Successfully generated and sent daily report.'))
