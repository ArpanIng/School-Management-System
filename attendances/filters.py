import django_filters
from django import forms
from django.db import models

from .models import Attendance


class AttendanceFilter(django_filters.FilterSet):
    attendance_date = django_filters.DateFilter(
        field_name="attendance_date",
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"}),
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=Attendance.AttendanceStatus.choices,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Attendance
        fields = ["attendance_date", "status"]
