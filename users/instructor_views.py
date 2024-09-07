from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.list import ListView

from courses.models import Class

from .forms import (
    InstructorForm,
    MyUserChangeForm,
    ProfileForm,
    RegistrationForm,
    InstructorFilterForm,
)
from .mixins import AdminRequiredMixin
from .models import Instructor


class InstructorListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Instructor
    context_object_name = "instructors"
    template_name = "users/instructors/instructor_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        queryset = super().get_queryset()
        # apply search query
        if query:
            queryset = queryset.filter(
                Q(profile__user__username__icontains=query)
                | Q(profile__user__first_name__icontains=query)
                | Q(profile__user__last_name__icontains=query)
                | Q(profile__user__email__icontains=query)
            )

        form = InstructorFilterForm(self.request.GET)
        if form.is_valid():
            qualification = form.cleaned_data.get("qualification")
            department = form.cleaned_data.get("department")
            state = form.cleaned_data.get("state")
            marital_status = form.cleaned_data.get("marital_status")
            gender = form.cleaned_data.get("gender")
            status = form.cleaned_data.get("status")
            # apply filters query
            if qualification:
                queryset = queryset.filter(qualification=qualification)
            if department:
                queryset = queryset.filter(department=department)
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
        total_instructors = self.get_queryset().count()
        context["total_instructors"] = total_instructors
        context["instructor_create_url"] = reverse_lazy("instructor_create")
        context["filter_form"] = InstructorFilterForm(self.request.GET)
        return context


class InstructorCreateView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "users/instructors/instructor_form.html"

    def get(self, request, *args, **kwargs):
        registration_form = RegistrationForm()
        profile_form = ProfileForm()
        instructor_form = InstructorForm()
        context = {
            "registration_form": registration_form,
            "profile_form": profile_form,
            "instructor_form": instructor_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        registration_form = RegistrationForm(self.request.POST)
        profile_form = ProfileForm(self.request.POST, self.request.FILES)
        instructor_form = InstructorForm(self.request.POST)

        if (
            registration_form.is_valid()
            and profile_form.is_valid()
            and instructor_form.is_valid()
        ):
            try:
                with transaction.atomic():
                    # Save the user form and get the user instance
                    user = registration_form.save()

                    # The Profile instance is automatically created by the signal
                    profile = user.profile
                    # Save/Update the profile with additional form data
                    profile_form = ProfileForm(self.request.POST, instance=profile)
                    profile_form.save()

                    # Save the instructor form
                    instructor = instructor_form.save(commit=False)
                    instructor.profile = profile
                    instructor.save()
                messages.success(request, "Instructor created successfully.")
                return redirect("instructor_list")
            except Exception as e:
                messages.error(request, f"Error creating new instructor: {e}")
        else:
            messages.error(request, "Error creating instructor.")

        context = {
            "registration_form": registration_form,
            "profile_form": profile_form,
            "instructor_form": instructor_form,
        }
        return render(request, self.template_name, context)


class InstructorUpdateView(LoginRequiredMixin, AdminRequiredMixin, View):
    template_name = "users/instructors/instructor_form.html"

    def get(self, request, *args, **kwargs):
        instructor_id = kwargs.get("instructor_id")
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        user = instructor.profile.user
        profile = instructor.profile

        user_form = MyUserChangeForm(instance=user)
        profile_form = ProfileForm(instance=profile)
        instructor_form = InstructorForm(instance=instructor)
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "instructor_form": instructor_form,
            "instructor": instructor,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        instructor_id = kwargs.get("instructor_id")
        instructor = get_object_or_404(Instructor, pk=instructor_id)
        user = instructor.profile.user
        profile = instructor.profile

        user_form = MyUserChangeForm(self.request.POST, instance=user)
        profile_form = ProfileForm(
            self.request.POST,
            self.request.FILES,
            instance=profile,
        )
        instructor_form = InstructorForm(self.request.POST, instance=instructor)

        if (
            user_form.is_valid()
            and profile_form.is_valid()
            and instructor_form.is_valid()
        ):
            try:
                with transaction.atomic():
                    # Save the user form
                    user = user_form.save()
                    # Save/Update the profile form data
                    profile_form.save()
                    # Save the instructor form
                    instructor_form.save()
                messages.success(request, "Instructor updated successfully.")
                return redirect("instructor_list")
            except Exception as e:
                messages.error(request, f"Error updating instructor data: {e}")
        else:
            messages.error(request, "Error updating instructor.")

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "instructor_form": instructor_form,
        }
        return render(request, self.template_name, context)


class InstructorClassView(ListView):
    """
    Return class assigned to the request instructor.
    """

    model = Class
    context_object_name = "classes"
    template_name = "courses/classes/instructor_class_list.html"

    def get_queryset(self):
        instructor = self.request.user.profile.instructor
        return Class.objects.filter(class_instructor=instructor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_classes = self.get_queryset().count()
        context["total_classes"] = total_classes
        return context
