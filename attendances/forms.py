from django import forms

from courses.models import Enrollment

from .models import Attendance

ATTENDANCE_STATUS_CHOICES = (
    ("PRE", "Present"),
    ("ABS", "Absent"),
)


# class AttendanceForm(forms.ModelForm):
#     status = forms.ChoiceField(
#         widget=forms.RadioSelect, choices=ATTENDANCE_STATUS_CHOICES
#     )

#     class Meta:
#         model = Attendance
#         fields = ["attendance_date", "student", "status", "remarks"]
#         widgets = {
#             "attendance_date": forms.DateInput(attrs={"type": "date"}),
#         }

#     def __init__(self, *args, **kwargs):
#         super(AttendanceForm, self).__init__(*args, **kwargs)
#         self.fields["remarks"].widget.attrs["class"] = "form-control"
