# Generated by Django 5.0.6 on 2024-07-01 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('employee', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeShift',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateField(verbose_name='shift from date')),
                ('from_time', models.TimeField(verbose_name='shift timing')),
                ('to_time', models.TimeField(verbose_name='shift to date')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('employee_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='employee.employee')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.locations')),
            ],
        ),
    ]