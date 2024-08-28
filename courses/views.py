from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from users.mixins import AdminRequiredMixin

from django_filters.views import FilterView

from .forms import (
    ClassForm,
    ClassInstructorAssignForm,
    CourseForm,
    CourseFilterForm,
    EnrollmentForm,
    TestForm,
)
from .filters import ClassFilter
from .models import Class, Course, Enrollment


class TestView(CreateView):
    form_class = TestForm
    template_name = "test.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CourseListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    model = Course
    queryset = Course.objects.all().select_related("program").order_by("-id")
    context_object_name = "courses"
    template_name = "courses/course_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()

        form = CourseFilterForm(self.request.GET)
        if form.is_valid():
            program = form.cleaned_data["program"]
            if program:
                print("------------------------------")
                print(program)
                # queryset = queryset.filter(program=program)
        #     if is_active == "1":
        #         queryset = queryset.filter(is_active=True)
        #     elif is_active == "0":
        #         queryset = queryset.filter(is_active=False)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_courses = self.get_queryset().count()
        context["total_courses"] = total_courses
        context["course_create_url"] = reverse_lazy("courses:course_create")
        context["filter_form"] = CourseFilterForm(self.request.GET)
        return context


def course(request):
    courses = Course.objects.all()
    # print("----------------")
    # print(data)
    data = {
        "courses": [
            {"id": course.id, "name": course.name, "slug": course.slug}
            for course in courses
        ]
    }
    return JsonResponse(data, safe=False)


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    queryset = Course.objects.all()
    context_object_name = "course"
    slug_field = "slug"
    slug_url_kwarg = "course_slug"
    template_name = "courses/course_detail.html"


class CourseCreateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Course
    context_object_name = "course"
    form_class = CourseForm
    success_message = "Course added successfully."
    success_url = reverse_lazy("courses:course_list")
    template_name = "courses/course_form.html"


class CourseUpdateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Course
    context_object_name = "course"
    form_class = CourseForm
    slug_field = "slug"
    slug_url_kwarg = "course_slug"
    success_message = "Course updated successfully."
    success_url = reverse_lazy("courses:course_list")
    template_name = "courses/course_form.html"


class CourseDeleteView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, DeleteView
):
    model = Course
    context_object_name = "course"
    form_class = CourseForm
    pk_url_kwarg = "course_id"
    success_message = "Course deleted successfully."
    success_url = reverse_lazy("courses:course_list")
    template_name = "departments/department_form.html"


class EnrollmentListView(ListView):
    model = Enrollment
    queryset = Enrollment.objects.all().order_by("-id")
    context_object_name = "enrollments"
    template_name = "courses/enrollments/enrollment_list.html"

    def get_queryset(self):
        return (
            super().get_queryset().select_related("student", "class_instance__course")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_enrollments = self.get_queryset().count()
        context["total_enrollments"] = total_enrollments
        context["enrollment_create_url"] = reverse_lazy("courses:enrollment_create")
        return context


class EnrollmentCreateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Enrollment
    context_object_name = "enrollment"
    form_class = EnrollmentForm
    success_message = "Enrollment added successfully."
    success_url = reverse_lazy("courses:enrollment_list")
    template_name = "courses/enrollments/enrollment_form.html"


class EnrollmentUpdateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Enrollment
    context_object_name = "enrollment"
    form_class = EnrollmentForm
    success_message = "Enrollment updated successfully."
    success_url = reverse_lazy("courses:enrollment_list")
    template_name = "courses/enrollments/enrollment_form.html"


class ClassListView(LoginRequiredMixin, AdminRequiredMixin, FilterView):
    model = Class
    context_object_name = "classes"
    filterset_class = ClassFilter
    template_name = "courses/classes/class_list.html"

    def get_queryset(self):
        return (
            Class.objects.all()
            .order_by("-created_at")
            .select_related("course", "semester", "class_instructor__profile__user")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_classes = self.get_queryset().count()
        context["total_classes"] = total_classes
        context["class_create_url"] = reverse_lazy("courses:class_create")
        return context


class ClassCreateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, CreateView
):
    model = Class
    context_object_name = "class"
    form_class = ClassForm
    success_message = "Class added successfully."
    success_url = reverse_lazy("courses:class_list")
    template_name = "courses/classes/class_form.html"


class ClassDetailView(LoginRequiredMixin, DetailView):
    model = Class
    queryset = Class.objects.all()
    context_object_name = "class"
    pk_url_kwarg = "class_id"
    template_name = "courses/classes/class_detail.html"

    # def dispatch(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     user = request.user
    #     # Check if the user is enrolled in the course
    #     if not self.object.is_enrolled(user):
    #         raise PermissionDenied("You are not enrolled in this course.")
    #     return super().dispatch(request, *args, **kwargs)

    # def get_queryset(self):
    #     return super().get_queryset().select_related

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        class_obj = self.object
        enrolled_students = class_obj.get_enrolled_students()
        enrolled_students_count = enrolled_students.count()
        context["enrolled_students"] = enrolled_students
        context["enrolled_students_count"] = enrolled_students_count
        return context


class ClassUpdateView(
    LoginRequiredMixin, AdminRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Class
    context_object_name = "class"
    form_class = ClassForm
    pk_url_kwarg = "class_id"
    success_message = "Class updated successfully."
    success_url = reverse_lazy("courses:class_list")
    template_name = "courses/classes/class_form.html"


class AssignClassInstructorView(LoginRequiredMixin, AdminRequiredMixin, View):
    """View to assign/update instructor of a class."""

    template_name = "courses/classes/class_instructor_assign.html"

    def get(self, request, *args, **kwargs):
        class_id = kwargs.get("class_id")
        class_instance = get_object_or_404(Class, pk=class_id)
        form = ClassInstructorAssignForm(instance=class_instance)
        context = {"form": form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        class_id = kwargs.get("class_id")
        class_instance = get_object_or_404(Class, pk=class_id)
        form = ClassInstructorAssignForm(self.request.POST, instance=class_instance)
        if form.is_valid():
            class_instructor = form.cleaned_data["class_instructor"]
            class_instance.class_instructor = class_instructor
            # only updates the single field instead of all fields
            class_instance.save(update_fields=["class_instructor"])
            messages.success(request, "Instructor assigned successfully.")
            return redirect("courses:class_list")
        else:
            messages.success(request, "Instructor assign failed.")
        return render(request, self.template_name)


class AssessmentListView(ListView):
    pass
