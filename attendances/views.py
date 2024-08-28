import calendar
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django_filters.views import FilterView

from courses.models import Class
from users.mixins import AdminRequiredMixin, InstructorRequiredMixin

from .filters import AttendanceFilter
from .models import Attendance


class ClassAttendanceListView(TemplateView):
    template_name = "attendances/class_attendance_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_month = datetime.now().month
        current_year = datetime.now().year
        days_in_month = calendar.monthrange(current_year, current_month)[
            1
        ]  # accessing the second tuple index
        days = range(1, days_in_month + 1)
        context["days_in_month"] = days_in_month
        context["days"] = days
        return context


# class ClassAttendanceListView(TemplateView):
# model = Attendance
# context_object_name = "attendances"
# filterset_class = AttendanceFilter
# template_name = "attendances/class_attendance_list.html"

# def get_queryset(self):
#     class_obj = self.kwargs.get("class_id")
#     return (
#         super()
#         .get_queryset()
#         .filter(course_class=class_obj)
#         .select_related("student__profile__user")
#     )


def take_attendance(request, class_id):
    """
    View to take/update attendance of a class on a selected date.
    """

    selected_class = Class.objects.get(id=class_id)
    enrolled_students = selected_class.get_enrolled_students()
    # Set the current date for the date input field
    current_date = timezone.localdate()
    # Format date as YYYY-MM-DD
    formatted_date = current_date.strftime("%Y-%m-%d")
    attendance_date = request.POST.get("attendance_date", formatted_date)

    if request.method == "POST":
        # Retrieve the date from POST data or use localdate
        attendance_date = request.POST.get("attendance_date", formatted_date)

        for student in enrolled_students:
            # default to current date (today)
            status = request.POST.get(f"attendance_{student.id}")
            remarks = request.POST.get(f"remarks_{student.id}", "")
            if status:
                Attendance.objects.create(
                    course_class=selected_class,
                    student=student,
                    attendance_date=attendance_date,
                    defaults={"status": status, "remarks": remarks},
                )
        return redirect("instructor_class_list")
    context = {
        "formatted_date": formatted_date,
        "selected_class": selected_class,
        "enrolled_students": enrolled_students,
    }
    return render(request, "attendances/class_attendance_take.html", context)


def update_attendance(request, class_id):
    """
    View to take/update attendance of a class on a selected date.
    """

    selected_class = Class.objects.get(id=class_id)
    enrolled_students = selected_class.get_enrolled_students()
    # Set the current date for the date input field
    current_date = timezone.localdate()
    # Format date as YYYY-MM-DD
    formatted_date = current_date.strftime("%Y-%m-%d")
    attendance_date = request.POST.get("attendance_date", formatted_date)

    # Fetch existing attendance records for the selected date
    existing_attendance = Attendance.objects.filter(
        course_class=selected_class, attendance_date=attendance_date
    ).select_related("student")
    attendance_dict = {att.student.student_id: att for att in existing_attendance}

    if request.method == "POST":
        # Retrieve the date from POST data or use localdate
        attendance_date = request.POST.get("attendance_date", formatted_date)

        for student in enrolled_students:
            # default to current date (today)
            status = request.POST.get(f"attendance_{student.id}")
            remarks = request.POST.get(f"remarks_{student.id}", "")
            if status:
                Attendance.objects.update_or_create(
                    course_class=selected_class,
                    student=student,
                    attendance_date=attendance_date,
                    defaults={"status": status, "remarks": remarks},
                )
        return redirect("instructor_class_list")
    context = {
        "formatted_date": formatted_date,
        "selected_class": selected_class,
        "enrolled_students": enrolled_students,
        "attendance_dict": attendance_dict,
    }
    return render(request, "attendances/class_attendance_update.html", context)


class ClassAttendanceTakeView(View):
    def get(self, request, class_id, *args, **kwargs):
        selected_class = get_object_or_404(Class, id=class_id)
        enrolled_students = selected_class.get_enrolled_students()
        context = {
            "selected_class": selected_class,
            "enrolled_students": enrolled_students,
        }
        return render(request, "attendances/class_attendance_take.html", context)

    def post(self, request, class_id, *args, **kwargs):
        return render(request, "attendances/class_attendance_take.html")


class ClassEnrolledStudents(View):
    pass


import json

from django.http import JsonResponse


def class_enrolled_students(request, class_id):
    class_obj = get_object_or_404(Class, id=class_id)
    print("--------------------")
    enrolled_students = class_obj.students.all()
    print(enrolled_students)
    return JsonResponse("hey", safe=False)
