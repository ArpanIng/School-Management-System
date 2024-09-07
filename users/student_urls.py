from django.urls import path

from . import student_views

student_urlpatterns = [
    path("students/", student_views.StudentListView.as_view(), name="student_list"),
    path(
        "students/add/",
        student_views.StudentCreateView.as_view(),
        name="student_create",
    ),
    path(
        "students/<int:student_id>/edit/",
        student_views.StudentUpdateView.as_view(),
        name="student_update",
    ),
    path(
        "students/academics/",
        student_views.StudentAcademicView.as_view(),
        name="student_academic_list",
    ),
    path(
        "enrolled/courses/",
        student_views.StudentEnrolledCoruses.as_view(),
        name="enrolled_courses",
    ),
]
