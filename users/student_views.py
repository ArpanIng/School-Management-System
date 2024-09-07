from typing import Any, Dict
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView

from courses.models import Enrollment
from .forms import (
    MyUserChangeForm,
    ProfileForm,
    RegistrationForm,
    StudentForm,
    StudentFilterForm,
)
from .mixins import AdminRequiredMixin, StudentRequiredMixin
from .models import Student

User = get_user_model()


class StudentListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Student
    context_object_name = "students"
    paginate_by = 50
    template_name = "users/students/student_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        # apply search query
        if query:
            queryset = queryset.filter(
                Q(profile__user__username__icontains=query)
                | Q(profile__user__first_name__icontains=query)
                | Q(profile__user__last_name__icontains=query)
                | Q(profile__user__email__icontains=query)
                | Q(guardian__icontains=query)
            )

        form = StudentFilterForm(self.request.GET)
        if form.is_valid():
            state = form.cleaned_data["state"]
            marital_status = form.cleaned_data["marital_status"]
            gender = form.cleaned_data["gender"]
            status = form.cleaned_data["status"]
            # apply filters query
            if state:
                queryset = queryset.filter(profile__state=state)
            if marital_status:
                queryset = queryset.filter(profile__marital_status=marital_status)
            if gender:
                queryset = queryset.filter(profile__gender=gender)
            if status:
                queryset = queryset.filter(status=status)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_students = self.get_queryset().count()
        context["total_students"] = total_students
        context["student_create_url"] = reverse_lazy("student_create")
        context["filter_form"] = StudentFilterForm(self.request.GET)
        return context


class StudentCreateView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "users/students/student_form.html"

    def get(self, request, *args, **kwargs):
        registration_form = RegistrationForm()
        profile_form = ProfileForm()
        student_form = StudentForm()
        context = {
            "registration_form": registration_form,
            "profile_form": profile_form,
            "student_form": student_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        registration_form = RegistrationForm(self.request.POST)
        profile_form = ProfileForm(self.request.POST, self.request.FILES)
        student_form = StudentForm(self.request.POST)

        if (
            registration_form.is_valid()
            and profile_form.is_valid()
            and student_form.is_valid()
        ):
            try:
                with transaction.atomic():
                    # Save the registration form and get the user instance
                    user = registration_form.save()

                    # The Profile instance is automatically created by the signal
                    profile = user.profile
                    # Save/Update the profile with additional form data
                    profile_form = ProfileForm(self.request.POST, instance=profile)
                    profile_form.save()

                    # Save the student form
                    student = student_form.save(commit=False)
                    student.profile = profile
                    student.save()
                messages.success(request, "Student created successfully.")
                return redirect("student_list")
            except Exception as e:
                messages.error(request, f"Error creating new student: {e}")
        else:
            messages.error(request, "Error creating student.")

        context = {
            "registration_form": registration_form,
            "profile_form": profile_form,
            "student_form": student_form,
        }
        return render(request, self.template_name, context)


class StudentUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "users/students/student_form.html"

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        student = get_object_or_404(Student, pk=student_id)
        user = student.profile.user
        profile = student.profile

        user_form = MyUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        student_form = StudentForm(instance=student)
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "student_form": student_form,
            "student": student,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        student = get_object_or_404(Student, pk=student_id)
        user = student.profile.user
        profile = student.profile

        user_form = MyUserChangeForm(self.request.POST, instance=user)
        profile_form = ProfileForm(
            self.request.POST,
            self.request.FILES,
            instance=profile,
        )
        student_form = StudentForm(self.request.POST, instance=student)

        if user_form.is_valid() and profile_form.is_valid() and student_form.is_valid():
            try:
                with transaction.atomic():
                    # Save the user form
                    user = user_form.save()
                    # Save/Update the profile form data
                    profile_form.save()
                    # Save the student form
                    student_form.save()
                messages.success(request, "Student updated successfully.")
                return redirect("student_list")
            except Exception as e:
                messages.error(request, f"Error updating student data: {e}")
        else:
            messages.error(request, "Error updating student.")

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "student_form": student_form,
        }
        return render(request, self.template_name, context)


class StudentEnrolledCoruses(LoginRequiredMixin, StudentRequiredMixin, TemplateView):
    template_name = "users/students/enrolled_courses.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        student = self.request.user.profile.student
        enrolled_classes = student.get_enrolled_classes().select_related(
            "class_instance__course"
        )
        context["enrolled_classes"] = enrolled_classes
        return context


class StudentAcademicView(LoginRequiredMixin, TemplateView):
    template_name = "users/students/academic_list.html"
