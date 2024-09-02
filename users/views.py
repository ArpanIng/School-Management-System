from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
)
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView

from .forms import ProfileForm, RegistrationForm, UserForm
from .mixins import AdminRequiredMixin
from .models import Profile

User = get_user_model()


class CustomLoginView(LoginView):
    template_name = "users/auth/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    pass


class CustomAdminPasswordChangeView(LoginRequiredMixin, AdminRequiredMixin, View):
    """
    A form used to change the password of a user in the admin interface by the 'Admin' group user.
    """

    template_name = "users/auth/admin_password_change_form.html"

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = get_object_or_404(User, pk=user_id)
        # The first parameter to the form instantiation call is supposed to be a user instance
        form = AdminPasswordChangeForm(user=user)
        context = {"form": form, "user": user}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get("user_id")
        user = get_object_or_404(User, id=user_id)
        form = AdminPasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("user_list")
        context = {"form": form, "user": user}
        return render(request, self.template_name, context)


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy("password_change_done")
    template_name = "users/auth/password_change_form.html"


class CustomPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "users/auth/password_change_done.html"


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """View to list all users."""

    model = get_user_model()
    context_object_name = "users"
    queryset = get_user_model().objects.all().order_by("-date_joined")
    template_name = "users/user_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_count"] = self.queryset.count()
        return context


class UserCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    View to create/register a new user into the system.
    """

    model = get_user_model()
    context_object_name = "user"
    form_class = RegistrationForm
    success_message = "User created successfully."
    template_name = "users/auth/register.html"

    def get_success_url(self):
        return reverse_lazy("user-profile-update", kwargs={"pk": self.object.pk})


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """View to update user of the system."""

    model = get_user_model()
    context_object_name = "user"
    form_class = UserForm
    success_message = "User updated successfully."
    success_url = reverse_lazy("user_list")
    template_name = "users/user_form.html"


class ProfileView(LoginRequiredMixin, DetailView):
    """
    View to display profile of a request user.
    """

    model = Profile
    context_object_name = "profile"
    template_name = "users/profile.html"

    def get_object(self, queryset=None):
        user = self.request.user
        return get_object_or_404(Profile.objects.select_related("user"), user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_role = None
        user = self.request.user

        # returns ListQuerySet of user's groups
        groups = user.groups.values_list("name", flat=True)

        if "Admin" in groups:
            user_role = "admin"
        elif "Instructor" in groups:
            user_role = "instructor"
        elif "Student" in groups:
            user_role = "student"

        context["user_role"] = user_role
        return context


class ProfileFormView(FormView):
    form_class = ProfileForm
    template_name = "users/profile_form.html"
    success_url = reverse_lazy("users-list")

    # def form_valid(self, form):
    #     form =
    #     return super().form_valid(form)


class ProfileEditView(LoginRequiredMixin, AdminRequiredMixin, View):
    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        u_form = UserForm(instance=user)
        p_form = ProfileForm(instance=user.profile)
        context = {
            "u_form": u_form,
            "p_form": p_form,
        }
        return render(request, "users/profile_form.html", context)

    def post(self, request, *args, **kwargs):
        u_form = UserForm(self.request.POST, instance=self.request.user)
        p_form = ProfileForm(
            self.request.POST, self.request.FILES, instance=self.request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("user_profile")
        context = {
            "u_form": u_form,
            "p_form": p_form,
        }
        return render(request, "users/profile_form.html", context)
