from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is in 'Admin' group."""

    permission_denied_message = "You do not have permission to access this admin page."

    def dispatch(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return self.handle_no_permission()

        if not self.request.user.groups.filter(name="Admin").exists():
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class InstructorRequiredMixin(AccessMixin):
    """Verify that the current user is in 'Instructor' group."""

    permission_denied_message = (
        "You do not have permission to access this instructor page."
    )

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="Instructor").exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        raise PermissionDenied(self.get_permission_denied_message())


class StudentRequiredMixin(AccessMixin):
    """Verify that the current user is in 'Student' group."""

    permission_denied_message = (
        "You do not have permission to access this student page."
    )

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.groups.filter(name="Student").exists():
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        raise PermissionDenied(self.get_permission_denied_message())


class NameSearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.reqeust.GET.get("q")
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset
