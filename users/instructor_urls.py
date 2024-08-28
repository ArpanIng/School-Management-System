from django.urls import path

from . import instructor_views as views

instructor_urlpatterns = [
    path("instructors/", views.InstructorListView.as_view(), name="instructor_list"),
    path(
        "instructors/add/",
        views.InstructorCreateView.as_view(),
        name="instructor_create",
    ),
    path(
        "instructors/<int:instructor_id>/edit/",
        views.InstructorUpdateView.as_view(),
        name="instructor_update",
    ),
    path(
        "instructors/classes/",
        views.InstructorClassView.as_view(),
        name="instructor_class_list",
    ),
]
