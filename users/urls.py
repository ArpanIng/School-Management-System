from django.urls import path

from . import views
from .instructor_urls import instructor_urlpatterns
from .student_urls import student_urlpatterns

# profile views urls
urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/add/", views.UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/edit/", views.UserUpdateView.as_view(), name="user_update"),
    path("users/profile/me/", views.ProfileView.as_view(), name="user_profile"),
    path(
        "users/<int:user_id>/password/",
        views.CustomAdminPasswordChangeView.as_view(),
        name="admin_password_change",
    ),
    path(
        "users/profile/<int:user_id>/edit/",
        views.ProfileEditView.as_view(),
        name="user_profile_edit",
    ),
]

# auth views urls
urlpatterns += [
    path("auth/login/", views.CustomLoginView.as_view(), name="login"),
    path("auth/logout/", views.CustomLogoutView.as_view(), name="logout"),
    path(
        "accounts/password-change/",
        views.CustomPasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "accounts/password-change/done/",
        views.CustomPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]

urlpatterns += student_urlpatterns
urlpatterns += instructor_urlpatterns
