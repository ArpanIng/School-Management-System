from django.urls import path

from . import views

app_name = "academics"

urlpatterns = [
    # department urls
    path("departments/", views.DepartmentListView.as_view(), name="department_list"),
    path(
        "departments/add/",
        views.DepartmentCreateView.as_view(),
        name="department_create",
    ),
    path(
        "departments/<int:pk>/edit/",
        views.DepartmentUpdateView.as_view(),
        name="department_update",
    ),
    path(
        "departments/<int:pk>/delete/",
        views.DepartmentDeleteView.as_view(),
        name="department_delete",
    ),
    # academicyear urls
    path(
        "academicyear/", views.AcademicYearListView.as_view(), name="academicyear_list"
    ),
    path(
        "academicyear/add/",
        views.AcademicYearCreateView.as_view(),
        name="academicyear_create",
    ),
    # semesters urls
    path("semesters/", views.SemesterListView.as_view(), name="semester_list"),
    path("semesters/add/", views.SemesterCreateView.as_view(), name="semester_create"),
    path(
        "semesters/<int:pk>/edit/",
        views.SemesterUpdateView.as_view(),
        name="semester_update",
    ),
    # program urls
    path("programs/", views.ProgramListView.as_view(), name="program_list"),
    path("programs/add/", views.ProgramCreateView.as_view(), name="program_create"),
    path(
        "programs/<slug:program_slug>/",
        views.ProgamDetailView.as_view(),
        name="program_detail",
    ),
    path(
        "programs/<slug:program_slug>/edit/",
        views.ProgramUpdateView.as_view(),
        name="program_update",
    ),
    path(
        "programs/<int:program_id>/delete/",
        views.ProgramDeleteView.as_view(),
        name="program_delete",
    ),
    path("", views.DashboardRouterView.as_view(), name="dashboard_router"),
    path("dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path(
        "dashboard/",
        views.InstructorDashboardView.as_view(),
        name="instructor_dashboard",
    ),
    path("home/", views.StudentDashboardView.as_view(), name="student_dashboard"),
]
