from django.urls import path

from attendances import views as att_views

from . import views

app_name = "courses"

urlpatterns = [
    # course urls
    path("tests/", views.TestView.as_view()),
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("courses/add/", views.CourseCreateView.as_view(), name="course_create"),
    path(
        "courses/<slug:course_slug>/",
        views.CourseDetailView.as_view(),
        name="course_detail",
    ),
    path(
        "courses/<slug:course_slug>/edit/",
        views.CourseUpdateView.as_view(),
        name="course_update",
    ),
    path(
        "courses/<int:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="course_delete",
    ),
    # enrollment urls
    path("enrollments/", views.EnrollmentListView.as_view(), name="enrollment_list"),
    path(
        "enrollments/add/",
        views.EnrollmentCreateView.as_view(),
        name="enrollment_create",
    ),
    path(
        "enrollments/<int:pk>/edit/",
        views.EnrollmentUpdateView.as_view(),
        name="enrollment_update",
    ),
    # path(
    #     "enrollments/<int:pk>/delete/",
    #     views.EnrollmentDeleteView.as_view(),
    #     name="enrollment-delete",
    # ),
    # class urls
    path("classes/", views.ClassListView.as_view(), name="class_list"),
    path("classes/new/", views.ClassCreateView.as_view(), name="class_create"),
    path(
        "classes/<int:class_id>/", views.ClassDetailView.as_view(), name="class_detail"
    ),
    path(
        "classes/<int:class_id>/edit/",
        views.ClassUpdateView.as_view(),
        name="class_update",
    ),
    path(
        "classes/<int:class_id>/assign-instructor/",
        views.AssignClassInstructorView.as_view(),
        name="class_instructor_assign",
    ),
    path(
        "classes/<int:class_id>/students/",
        att_views.class_enrolled_students,
        name="class_enrolled_students",
    ),
    path(
        "classes/<int:class_id>/attendances/",
        att_views.ClassAttendanceListView.as_view(),
        name="class_attendance_list",
    ),
    path(
        "classes/<int:class_id>/attendances/take/",
        att_views.take_attendance,
        name="class_take_attendance",
    ),
    path(
        "classes/<int:class_id>/attendances/update/",
        att_views.update_attendance,
        name="class_update_attendance",
    ),
]
