from typing import Any, Dict
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.base import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from courses.models import Course
from users.mixins import (
    AdminRequiredMixin,
    InstructorRequiredMixin,
    StudentRequiredMixin,
)
from users.models import Instructor, Student
from courses.models import Class, Enrollment

from .forms import (
    AcademicYearForm,
    DepartmentForm,
    ProgramForm,
    ProgramFilterForm,
    SemesterForm,
)
from .models import AcademicYear, Department, Program, Semester
from .utils import get_user_role_by_group


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    A view which displays data based on the user's group.
    """

    def get_template_names(self) -> list[str]:
        user = self.request.user
        user_role = get_user_role_by_group(user=user)
        if user_role == "admin":
            return ["academics/dashboard_admin.html"]
        elif user_role == "instructor":
            return ["academics/dashboard_instructor.html"]
        elif user_role == "student":
            return ["academics/dashboard_student.html"]
        return super().get_template_names()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        user_role = get_user_role_by_group(user=user)
        if user_role == "admin":
            context["dashboard_data"] = self.get_admin_dashboard_data()
        elif user_role == "instructor":
            context["dashboard_data"] = self.get_instructor_dashboard_data()
        elif user_role == "student":
            context["dashboard_data"] = self.get_student_dashboard_data()
        return context

    def get_admin_dashboard_data(self):
        # card data
        instructors_count = Instructor.objects.all().count()
        students_count = Student.objects.all().count()
        courses_count = Course.objects.all().count()
        departments_count = Department.objects.all().count()
        programs_count = Program.objects.all().count()

        # chart data
        user_type_list = ["Instructor", "Student"]
        user_type_list_number = [instructors_count, students_count]

        data = {
            "total_instructors": instructors_count,
            "total_students": students_count,
            "total_courses": courses_count,
            "total_deparments": departments_count,
            "total_programs": programs_count,
            "user_type_list": user_type_list,
            "user_type_list_number": user_type_list_number,
        }
        return data

    def get_instructor_dashboard_data(self):
        instructor = self.request.user.profile.instructor
        assigned_classes_count = Class.objects.filter(
            class_instructor=instructor
        ).count()
        data = {
            "assigned_classes_count": assigned_classes_count,
        }
        return data

    def get_student_dashboard_data(self):
        student = self.request.user.profile.student
        enrolled_classes_count = student.get_enrolled_classes().count()
        data = {
            "enrolled_classes_count": enrolled_classes_count,
        }
        return data


class DepartmentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Department
    queryset = Department.objects.all().order_by("id")
    context_object_name = "departments"
    template_name = "academics/departments/department_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_departments = self.get_queryset().count()
        context["total_departments"] = total_departments
        context["department_create_url"] = reverse_lazy("academics:department_create")
        return context


class DepartmentCreateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView
):
    """View for creating a department."""

    model = Department
    context_object_name = "department"
    form_class = DepartmentForm
    success_message = "Department created successfully."
    success_url = reverse_lazy("academics:department_list")
    template_name = "academics/departments/department_form.html"


class DepartmentUpdateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView
):
    """View for updating a department."""

    model = Department
    context_object_name = "department"
    form_class = DepartmentForm
    success_message = "Department updated successfully."
    success_url = reverse_lazy("academics:department_list")
    template_name = "academics/departments/department_form.html"


class DepartmentDeleteView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, DeleteView
):
    """View for deleting a department."""

    model = Department
    context_object_name = "department"
    success_message = "Department deleted successfully."
    success_url = reverse_lazy("academics:department_list")
    template_name = "academics/departments/department_delete_modal.html"


class AcademicYearListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = AcademicYear
    queryset = AcademicYear.objects.all().order_by("-year")
    context_object_name = "academicyears"
    template_name = "academics/academicyears/academicyear_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_academicyears = self.get_queryset().count()
        context["total_academicyears"] = total_academicyears
        context["academicyear_create_url"] = reverse_lazy(
            "academics:academicyear_create"
        )
        return context


class AcademicYearCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = AcademicYear
    context_object_name = "academicyear"
    form_class = AcademicYearForm
    success_message = "Academic year created successfully."
    success_url = reverse_lazy("academics:academicyear_list")
    template_name = "academics/academicyears/academicyear_form.html"


class SemesterListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Semester
    context_object_name = "semesters"
    template_name = "academics/semesters/semester_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_semesters = self.get_queryset().count()
        context["total_semesters"] = total_semesters
        context["semester_create_url"] = reverse_lazy("academics:semester_create")
        return context


class SemesterCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    model = Semester
    context_object_name = "semester"
    form_class = SemesterForm
    success_message = "Semester created successfully."
    success_url = reverse_lazy("academics:semester_list")
    template_name = "academics/semesters/semester_form.html"


class SemesterUpdateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView
):
    """View for updating a semester."""

    model = Semester
    context_object_name = "semester"
    form_class = SemesterForm
    success_message = "Semester updated successfully."
    success_url = reverse_lazy("academics:semester_list")
    template_name = "academics/semesters/semester_form.html"


class ProgramListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Program
    queryset = Program.objects.all().order_by("id")
    context_object_name = "programs"
    template_name = "academics/programs/program_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        form = ProgramFilterForm(self.request.GET)
        if form.is_valid():
            department = form.cleaned_data["department"]
            degree_type = form.cleaned_data["degree_type"]
            is_active = form.cleaned_data["is_active"]
            if department:
                queryset = queryset.filter(department=department)
            if degree_type:
                queryset = queryset.filter(degree_type=degree_type)
            if is_active == "1":
                queryset = queryset.filter(is_active=True)
            elif is_active == "0":
                queryset = queryset.filter(is_active=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_programs = self.get_queryset().count()
        context["total_programs"] = total_programs
        context["program_create_url"] = reverse_lazy("academics:program_create")
        context["filter_form"] = ProgramFilterForm(self.request.GET)
        return context


class ProgramCreateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView
):
    """View for creating a program."""

    model = Program
    context_object_name = "program"
    form_class = ProgramForm
    success_message = "Program created successfully."
    success_url = reverse_lazy("academics:program_list")
    template_name = "academics/programs/program_form.html"


class ProgamDetailView(LoginRequiredMixin, DetailView):
    model = Program
    context_object_name = "program"
    slug_field = "slug"
    slug_url_kwarg = "program_slug"
    template_name = "academics/programs/program_detail.html"


class ProgramUpdateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView
):
    """View for updating a program."""

    model = Program
    context_object_name = "program"
    form_class = ProgramForm
    slug_field = "slug"
    slug_url_kwarg = "program_slug"
    success_message = "Program updated successfully."
    success_url = reverse_lazy("academics:program_list")
    template_name = "academics/programs/program_form.html"


class ProgramDeleteView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, DeleteView
):
    """View for deleting a program."""

    model = Program
    context_object_name = "program"
    pk_url_kwarg = "program_id"
    success_message = "Program deleted successfully."
    success_url = reverse_lazy("academics:program_list")
    template_name = "academics/programs/program_delete_modal.html"
